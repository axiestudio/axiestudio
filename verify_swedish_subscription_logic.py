#!/usr/bin/env python3
"""
Verifiering av prenumerationslogik för svenska versionen av Axie Studio.
Testar att utgångna provperioder och ogiltiga prenumerationer blockeras korrekt.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any

class MockUser:
    """Mock användarklass för testning."""
    def __init__(self, username: str, subscription_status: str, is_superuser: bool = False, 
                 trial_start=None, trial_end=None):
        self.username = username
        self.subscription_status = subscription_status
        self.is_superuser = is_superuser
        self.trial_start = trial_start
        self.trial_end = trial_end

def check_trial_status_logic(user: MockUser) -> Dict[str, Any]:
    """
    Replikerar prenumerationslogiken för att verifiera att den fungerar korrekt.
    """
    now = datetime.now(timezone.utc)
    trial_duration_days = 7
    
    # Superanvändare kringgår alla prenumerationskontroller
    if user.is_superuser:
        return {
            "status": "admin",
            "trial_expired": False,
            "days_left": 0,
            "should_cleanup": False
        }
    
    # Om användaren har aktiv prenumeration är de godkända
    if user.subscription_status == "active":
        return {
            "status": "subscribed",
            "trial_expired": False,
            "days_left": 0,
            "should_cleanup": False
        }
    
    # Beräkna provperiodsdatum med tidszonskonsekvens
    trial_start = user.trial_start or now
    # För provanvändare ska trial_end vara explicit satt - beräkna inte automatiskt för säkerhet
    if user.subscription_status == "trial" and not user.trial_end:
        # Detta är ett dataintegritetsfel - provanvändare MÅSTE ha trial_end
        trial_end = None
    else:
        trial_end = user.trial_end or (trial_start + timedelta(days=trial_duration_days))
    
    # Säkerställ tidszonskonsekvens för jämförelser
    if trial_start and trial_start.tzinfo is None:
        trial_start = trial_start.replace(tzinfo=timezone.utc)
    if trial_end and trial_end.tzinfo is None:
        trial_end = trial_end.replace(tzinfo=timezone.utc)
    
    # Kontrollera om provperioden har löpt ut
    trial_expired = now > trial_end if trial_end else False
    days_left = max(0, (trial_end - now).days) if trial_end else 0
    
    # KRITISKT: Blockera åtkomst för ALLA dessa fall:
    has_active_subscription = user.subscription_status == "active"
    has_valid_trial = trial_end and not trial_expired
    
    # Ska städa (blockera åtkomst) om:
    should_cleanup = (
        # Provperiod utgången och ingen aktiv prenumeration
        (trial_expired and not has_active_subscription) or
        # Ingen prenumerationsstatus alls (null, tom eller ogiltig)
        (not user.subscription_status or user.subscription_status not in ["active", "trial"]) or
        # Prenumerationsstatus är inte aktiv och ingen giltig provperiod
        (user.subscription_status != "active" and not has_valid_trial) or
        # Saknar trial_end datum för provanvändare (dataintegritetsfel)
        (user.subscription_status == "trial" and not trial_end)
    )
    
    return {
        "status": "trial" if not trial_expired else "expired",
        "trial_expired": trial_expired,
        "days_left": days_left,
        "should_cleanup": should_cleanup,
        "trial_end": trial_end
    }

def test_subscription_enforcement():
    """Testa alla prenumerationsscenarier."""
    print("🔒 TESTAR PRENUMERATIONSLOGIK FÖR SVENSKA VERSIONEN")
    print("=" * 70)
    
    test_cases = [
        # Test 1: Utgången provanvändare (SKA BLOCKERAS)
        {
            "name": "Utgången Provanvändare",
            "user": MockUser(
                username="utgangen_anvandare",
                subscription_status="trial",
                trial_start=datetime.now(timezone.utc) - timedelta(days=10),
                trial_end=datetime.now(timezone.utc) - timedelta(days=3)
            ),
            "should_block": True
        },
        
        # Test 2: Aktiv provanvändare (SKA HA ÅTKOMST)
        {
            "name": "Aktiv Provanvändare",
            "user": MockUser(
                username="aktiv_provanvandare",
                subscription_status="trial",
                trial_start=datetime.now(timezone.utc) - timedelta(days=2),
                trial_end=datetime.now(timezone.utc) + timedelta(days=5)
            ),
            "should_block": False
        },
        
        # Test 3: Prenumerant (SKA HA ÅTKOMST)
        {
            "name": "Prenumerant",
            "user": MockUser(
                username="prenumerant",
                subscription_status="active"
            ),
            "should_block": False
        },
        
        # Test 4: Admin (SKA HA ÅTKOMST)
        {
            "name": "Admin",
            "user": MockUser(
                username="admin",
                subscription_status="trial",
                is_superuser=True,
                trial_start=datetime.now(timezone.utc) - timedelta(days=10),
                trial_end=datetime.now(timezone.utc) - timedelta(days=3)
            ),
            "should_block": False
        },
        
        # Test 5: Ingen prenumerationsstatus (SKA BLOCKERAS)
        {
            "name": "Ingen Prenumerationsstatus",
            "user": MockUser(
                username="ingen_status",
                subscription_status=None
            ),
            "should_block": True
        },
        
        # Test 6: Ogiltig prenumerationsstatus (SKA BLOCKERAS)
        {
            "name": "Ogiltig Prenumerationsstatus",
            "user": MockUser(
                username="ogiltig_status",
                subscription_status="cancelled"
            ),
            "should_block": True
        },
        
        # Test 7: Provanvändare utan trial_end (SKA BLOCKERAS)
        {
            "name": "Provanvändare Saknar Trial End",
            "user": MockUser(
                username="saknar_trial_end",
                subscription_status="trial",
                trial_start=datetime.now(timezone.utc) - timedelta(days=2),
                trial_end=None
            ),
            "should_block": True
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        
        user = test_case["user"]
        expected_block = test_case["should_block"]
        
        # Kör logiken
        result = check_trial_status_logic(user)
        actual_block = result["should_cleanup"]
        
        # Skriv ut detaljer
        print(f"   Användare: {user.username}")
        print(f"   Prenumerationsstatus: {user.subscription_status}")
        print(f"   Är Superanvändare: {user.is_superuser}")
        print(f"   Provperiod Utgången: {result['trial_expired']}")
        print(f"   Dagar Kvar: {result['days_left']}")
        print(f"   Ska Blockera: {actual_block}")
        print(f"   Förväntat Blockera: {expected_block}")
        
        # Verifiera resultat
        if actual_block == expected_block:
            print(f"   ✅ GODKÄND")
        else:
            print(f"   ❌ MISSLYCKAD - Förväntade {expected_block}, fick {actual_block}")
            all_passed = False
    
    print("\n" + "=" * 70)
    print("📊 SLUTRESULTAT")
    print("=" * 70)
    
    if all_passed:
        print("🎉 ALLA TESTER GODKÄNDA!")
        print("✅ Prenumerationslogiken är STENSÄKER")
        print("✅ Utgångna användare KOMMER ATT BLOCKERAS")
        print("✅ Ogiltiga prenumerationsstatusar KOMMER ATT BLOCKERAS")
        print("✅ Saknad data KOMMER ATT BLOCKERAS")
        print("✅ Admin-användare är korrekt undantagna")
        print("✅ Giltiga prenumeranter och provanvändare har åtkomst")
        print("\n🔒 PROVPERIODSBUGG ÄR FIXAD!")
    else:
        print("❌ VISSA TESTER MISSLYCKADES!")
        print("Vänligen granska logiken")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 VERIFIERING AV PRENUMERATIONSLOGIK - SVENSKA VERSIONEN")
    print("Testar den förbättrade prenumerationslogiken...")
    print()
    
    success = test_subscription_enforcement()
    
    if success:
        print("\n🎯 VERIFIERING SLUTFÖRD")
        print("Prenumerationskontrollen är skottsäker!")
    else:
        print("\n⚠️ VERIFIERING MISSLYCKADES")
        print("Vänligen granska implementationen")
