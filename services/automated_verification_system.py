#!/usr/bin/env python3
"""
Automated Email Verification System
This system will:
1. Automatically detect and fix broken email verifications
2. Run as a background task to monitor verification issues
3. Provide proper logging and error handling
4. Ensure users are properly activated after email verification
"""

import asyncio
from datetime import datetime, timezone, timedelta


def ensure_timezone_aware(dt: datetime | None) -> datetime | None:
    """
    Ensure a datetime is timezone-aware.

    This fixes the common issue where database datetimes are stored as naive
    but need to be compared with timezone-aware datetimes.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # Assume naive datetimes are in UTC (database default)
        return dt.replace(tzinfo=timezone.utc)

    return dt

async def automated_verification_monitor():
    """Monitor and fix email verification issues automatically."""
    
    try:
        from axiestudio.services.deps import get_db_service
        from axiestudio.services.database.models.user.model import User
        from sqlmodel import select
        from loguru import logger
        
        print("🤖 Startar automatiserad e-postverifieringsmonitor")
        print("=" * 60)
        
        db_service = get_db_service()
        
        async with db_service.with_session() as session:
            
            # 1. Find users who should be verified but aren't
            print("🔍 Söker efter verifieringsproblem...")
            
            # Users with expired tokens but still unverified
            expired_token_stmt = select(User).where(
                User.email_verification_expires < datetime.now(timezone.utc),
                User.email_verified == False,
                User.email_verification_token.is_not(None)
            )
            expired_token_users = (await session.exec(expired_token_stmt)).all()
            
            # Users who are verified but not active
            verified_inactive_stmt = select(User).where(
                User.email_verified == True,
                User.is_active == False
            )
            verified_inactive_users = (await session.exec(verified_inactive_stmt)).all()
            
            # Users who are active but not verified (shouldn't happen)
            active_unverified_stmt = select(User).where(
                User.is_active == True,
                User.email_verified == False
            )
            active_unverified_users = (await session.exec(active_unverified_stmt)).all()
            
            total_issues = len(expired_token_users) + len(verified_inactive_users) + len(active_unverified_users)
            
            if total_issues == 0:
                print("✅ Inga verifieringsproblem hittades!")
                return True

            print(f"🚨 Hittade {total_issues} verifieringsproblem:")
            print(f"   - {len(expired_token_users)} användare med utgångna tokens")
            print(f"   - {len(verified_inactive_users)} verifierade men inaktiva användare")
            print(f"   - {len(active_unverified_users)} aktiva men overifierade användare")
            
            # 2. Fix expired token users (auto-verify if token expired recently)
            fixed_count = 0
            
            for user in expired_token_users:
                # If token expired within last 7 days, auto-verify
                if user.email_verification_expires:
                    # Ensure timezone-aware comparison
                    user_expires = ensure_timezone_aware(user.email_verification_expires)
                    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

                    if user_expires and user_expires > seven_days_ago:
                        print(f"🔧 Auto-verifierar användare med nyligen utgången token: {user.username}")
                        user.email_verified = True
                        user.is_active = True
                        user.email_verification_token = None
                        user.email_verification_expires = None
                        user.updated_at = datetime.now(timezone.utc)
                        fixed_count += 1
                    else:
                        print(f"⚠️  Användare {user.username} har mycket gammal utgången token - behöver manuell granskning")
                else:
                    print(f"⚠️  Användare {user.username} har inget utgångsdatum - behöver manuell granskning")
            
            # 3. Fix verified but inactive users
            for user in verified_inactive_users:
                print(f"🔧 Aktiverar verifierad användare: {user.username}")
                user.is_active = True
                user.updated_at = datetime.now(timezone.utc)
                fixed_count += 1
            
            # 4. Fix active but unverified users
            for user in active_unverified_users:
                print(f"🔧 Markerar aktiv användare som verifierad: {user.username}")
                user.email_verified = True
                user.email_verification_token = None
                user.email_verification_expires = None
                user.updated_at = datetime.now(timezone.utc)
                fixed_count += 1
            
            # 5. Commit all fixes
            if fixed_count > 0:
                try:
                    await session.commit()
                    print(f"✅ Fixade framgångsrikt {fixed_count} verifieringsproblem!")

                    # Log the fixes for audit trail
                    logger.info(f"Automatiserat verifieringssystem fixade {fixed_count} användarverifieringsproblem")

                except Exception as e:
                    await session.rollback()
                    print(f"❌ Misslyckades med att genomföra fixar: {e}")
                    logger.error(f"Misslyckades med att genomföra automatiserade verifieringsfixar: {e}")
                    return False
            
            # 6. Generate summary report
            print("\n📊 HÄLSORAPPORT FÖR VERIFIERINGSSYSTEM")
            print("=" * 40)
            
            # Check overall system health
            total_users_stmt = select(User)
            total_users = len((await session.exec(total_users_stmt)).all())
            
            verified_active_stmt = select(User).where(
                User.email_verified == True,
                User.is_active == True
            )
            verified_active_users = len((await session.exec(verified_active_stmt)).all())
            
            pending_verification_stmt = select(User).where(
                User.email_verified == False,
                User.email_verification_token.is_not(None)
            )
            pending_users = len((await session.exec(pending_verification_stmt)).all())
            
            print(f"Totalt antal användare: {total_users}")
            print(f"Verifierade & aktiva: {verified_active_users}")
            print(f"Väntar på verifiering: {pending_users}")
            if total_users > 0:
                print(f"Systemhälsa: {(verified_active_users/total_users*100):.1f}% verifierade")

            if pending_users > 0:
                print(f"\n⚠️  {pending_users} användare behöver fortfarande verifiera sin e-post")
            
            return True
            
    except Exception as e:
        print(f"❌ Automatiserad verifieringsmonitor misslyckades: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_verification_health_check():
    """Run a quick health check of the verification system."""

    try:
        from axiestudio.services.deps import get_db_service
        from axiestudio.services.database.models.user.model import User
        from sqlmodel import select

        print("🏥 Hälsokontroll för e-postverifieringssystem")
        print("=" * 50)

        db_service = get_db_service()

        async with db_service.with_session() as session:

            # Check for common issues
            issues = []

            # Issue 1: Users verified but not active
            stmt = select(User).where(User.email_verified == True, User.is_active == False)
            verified_inactive = (await session.exec(stmt)).all()
            if verified_inactive:
                issues.append(f"{len(verified_inactive)} verifierade användare är inte aktiva")

            # Issue 2: Users active but not verified
            stmt = select(User).where(User.is_active == True, User.email_verified == False)
            active_unverified = (await session.exec(stmt)).all()
            if active_unverified:
                issues.append(f"{len(active_unverified)} aktiva användare är inte verifierade")

            # Issue 3: Expired tokens
            stmt = select(User).where(
                User.email_verification_expires < datetime.now(timezone.utc),
                User.email_verified == False
            )
            expired_tokens = (await session.exec(stmt)).all()
            if expired_tokens:
                issues.append(f"{len(expired_tokens)} användare har utgångna verifieringstokens")

            if issues:
                print("🚨 PROBLEM HITTADE:")
                for issue in issues:
                    print(f"   - {issue}")
                print("\n💡 Kör automated_verification_monitor() för att fixa dessa problem")
                return False
            else:
                print("✅ E-postverifieringssystemet är friskt!")
                return True

    except Exception as e:
        print(f"❌ Hälsokontroll misslyckades: {e}")
        return False


if __name__ == "__main__":
    print("🤖 Automatiserat e-postverifieringssystem")
    print("Välj ett alternativ:")
    print("1. Kör hälsokontroll")
    print("2. Kör automatiserad monitor och fix")

    choice = input("Ange val (1 eller 2): ").strip()

    if choice == "1":
        success = asyncio.run(run_verification_health_check())
    elif choice == "2":
        success = asyncio.run(automated_verification_monitor())
    else:
        print("Ogiltigt val")
        success = False

    if success:
        print("\n🎉 Systemkontroll slutförd framgångsrikt!")
    else:
        print("\n❌ Systemkontroll hittade problem som behöver uppmärksamhet.")
