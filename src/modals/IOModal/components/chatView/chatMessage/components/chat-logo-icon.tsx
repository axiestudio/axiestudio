export default function LogoIcon() {
  return (
    <div className="relative flex h-8 w-8 items-center justify-center rounded-md bg-muted">
      <div className="flex h-8 w-8 items-center justify-center">
        <img
          src="/logo192.png"
          alt="Axie Studio Logo"
          className="absolute h-[18px] w-[18px] rounded object-contain"
          onError={(e) => {
            // Fallback to text logo if image fails to load
            e.currentTarget.style.display = 'none';
            e.currentTarget.nextElementSibling.style.display = 'flex';
          }}
          style={{ maxWidth: '18px', maxHeight: '18px' }}
        />
        <div
          className="absolute h-[18px] w-[18px] bg-primary text-primary-foreground rounded flex items-center justify-center font-bold text-[10px]"
          style={{ display: 'none' }}
        >
          AX
        </div>
      </div>
    </div>
  );
}
