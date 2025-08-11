function sortByName(stringList: string[]): string[] {
  return stringList.sort((a, b) => a.localeCompare(b));
 }


export default sortByName;
export { sortByName };