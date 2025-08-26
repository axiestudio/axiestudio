const NoResultsMessage = ({
  onClearSearch,
  message = "Inga komponenter hittades.",
  clearSearchText = "Rensa din sökning",
  additionalText = "eller filtrera och prova en annan fråga.",
}) => {
  return (
    <div className="flex h-full flex-col items-center justify-center p-3 text-center">
      <p className="text-sm text-secondary-foreground">
        {message}{" "}
        <a
          className="cursor-pointer underline underline-offset-4"
          onClick={onClearSearch}
        >
          {clearSearchText}
        </a>{" "}
        {additionalText}
      </p>
    </div>
  );
};

export default NoResultsMessage;
