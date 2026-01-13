# Obsidian Bases: Functions Reference

Complete function signatures and usage for all available functions in Obsidian Bases formulas.

## Global Functions

| Function       | Signature                                 | Description                                         |
| -------------- | ----------------------------------------- | --------------------------------------------------- |
| `date()`       | `date(string): date`                      | Parse string to date. Format: `YYYY-MM-DD HH:mm:ss` |
| `duration()`   | `duration(string): duration`              | Parse duration string                               |
| `now()`        | `now(): date`                             | Current date and time                               |
| `today()`      | `today(): date`                           | Current date (time = 00:00:00)                      |
| `if()`         | `if(condition, trueResult, falseResult?)` | Conditional                                         |
| `min()`        | `min(n1, n2, ...): number`                | Smallest number                                     |
| `max()`        | `max(n1, n2, ...): number`                | Largest number                                      |
| `number()`     | `number(any): number`                     | Convert to number                                   |
| `link()`       | `link(path, display?): Link`              | Create a link                                       |
| `list()`       | `list(element): List`                     | Wrap in list if not already                         |
| `file()`       | `file(path): file`                        | Get file object                                     |
| `image()`      | `image(path): image`                      | Create image for rendering                          |
| `icon()`       | `icon(name): icon`                        | Lucide icon by name                                 |
| `html()`       | `html(string): html`                      | Render as HTML                                      |
| `escapeHTML()` | `escapeHTML(string): string`              | Escape HTML characters                              |

## Any Type Functions

Available on any value:

| Function     | Signature                   | Description       |
| ------------ | --------------------------- | ----------------- |
| `isTruthy()` | `any.isTruthy(): boolean`   | Coerce to boolean |
| `isType()`   | `any.isType(type): boolean` | Check type        |
| `toString()` | `any.toString(): string`    | Convert to string |

## Date Functions

**Fields:** `date.year`, `date.month`, `date.day`, `date.hour`, `date.minute`, `date.second`, `date.millisecond`

| Function     | Signature                     | Description                   |
| ------------ | ----------------------------- | ----------------------------- |
| `date()`     | `date.date(): date`           | Remove time portion           |
| `format()`   | `date.format(string): string` | Format with Moment.js pattern |
| `time()`     | `date.time(): string`         | Get time as string            |
| `relative()` | `date.relative(): string`     | Human-readable relative time  |
| `isEmpty()`  | `date.isEmpty(): boolean`     | Always false for dates        |

## String Functions

**Field:** `string.length`

| Function        | Signature                                      | Description            |
| --------------- | ---------------------------------------------- | ---------------------- |
| `contains()`    | `string.contains(value): boolean`              | Check substring        |
| `containsAll()` | `string.containsAll(...values): boolean`       | All substrings present |
| `containsAny()` | `string.containsAny(...values): boolean`       | Any substring present  |
| `startsWith()`  | `string.startsWith(query): boolean`            | Starts with query      |
| `endsWith()`    | `string.endsWith(query): boolean`              | Ends with query        |
| `isEmpty()`     | `string.isEmpty(): boolean`                    | Empty or not present   |
| `lower()`       | `string.lower(): string`                       | To lowercase           |
| `title()`       | `string.title(): string`                       | To Title Case          |
| `trim()`        | `string.trim(): string`                        | Remove whitespace      |
| `replace()`     | `string.replace(pattern, replacement): string` | Replace pattern        |
| `repeat()`      | `string.repeat(count): string`                 | Repeat string          |
| `reverse()`     | `string.reverse(): string`                     | Reverse string         |
| `slice()`       | `string.slice(start, end?): string`            | Substring              |
| `split()`       | `string.split(delimiter): list`                | Split into list        |
| `join()`        | `string.join(other): string`                   | Join list elements     |

## Number Functions

| Function    | Signature                        | Description         |
| ----------- | -------------------------------- | ------------------- |
| `abs()`     | `number.abs(): number`           | Absolute value      |
| `ceil()`    | `number.ceil(): number`          | Round up            |
| `floor()`   | `number.floor(): number`         | Round down          |
| `round()`   | `number.round(digits?): number`  | Round to N decimals |
| `sqrt()`    | `number.sqrt(): number`          | Square root         |
| `pow()`     | `number.pow(exponent): number`   | Raise to power      |
| `min()`     | `number.min(other): number`      | Smaller of two      |
| `max()`     | `number.max(other): number`      | Larger of two       |
| `clamp()`   | `number.clamp(min, max): number` | Constrain to range  |
| `toFixed()` | `number.toFixed(digits): string` | Fixed decimals      |

## List Functions

| Function     | Signature                       | Description            |
| ------------ | ------------------------------- | ---------------------- |
| `first()`    | `list.first(): any`             | First element          |
| `last()`     | `list.last(): any`              | Last element           |
| `at()`       | `list.at(index): any`           | Element at index       |
| `length`     | `list.length: number`           | Number of elements     |
| `reverse()`  | `list.reverse(): list`          | Reverse order          |
| `sort()`     | `list.sort(): list`             | Sort ascending         |
| `map()`      | `list.map(fn): list`            | Transform each element |
| `filter()`   | `list.filter(fn): list`         | Keep matching elements |
| `find()`     | `list.find(fn): any`            | First matching element |
| `includes()` | `list.includes(value): boolean` | Contains value         |
| `isEmpty()`  | `list.isEmpty(): boolean`       | Empty or not present   |
| `join()`     | `list.join(separator): string`  | Join as string         |
| `concat()`   | `list.concat(other): list`      | Combine lists          |
| `flatten()`  | `list.flatten(): list`          | Flatten nested lists   |
| `unique()`   | `list.unique(): list`           | Remove duplicates      |

## List Aggregation Functions

| Function    | Parameter Type | Return Type | Description               |
| ----------- | -------------- | ----------- | ------------------------- |
| `Sum`       | Number         | Number      | Total of all values       |
| `Count`     | Any            | Number      | Count of non-empty values |
| `Average`   | Number         | Number      | Mathematical average      |
| `Min`       | Number         | Number      | Smallest value            |
| `Max`       | Number         | Number      | Largest value             |
| `Median`    | Number         | Number      | Mathematical median       |
| `Stddev`    | Number         | Number      | Standard deviation        |
| `Earliest`  | Date           | Date        | Earliest date             |
| `Latest`    | Date           | Date        | Latest date               |
| `Range`     | Date           | Date        | Latest - Earliest         |
| `Checked`   | Boolean        | Number      | Count of true values      |
| `Unchecked` | Boolean        | Number      | Count of false values     |
| `Empty`     | Any            | Number      | Count of empty values     |
| `Filled`    | Any            | Number      | Count of non-empty values |
| `Unique`    | Any            | Number      | Count of unique values    |

## File Functions

Functions available on `file` objects:

| Function     | Signature                      | Description        |
| ------------ | ------------------------------ | ------------------ |
| `hasTag()`   | `file.hasTag(tag): boolean`    | Has specific tag   |
| `hasLink()`  | `file.hasLink(link): boolean`  | Has link to target |
| `inFolder()` | `file.inFolder(path): boolean` | In specific folder |

### File Properties

| Property          | Type   | Description                 |
| ----------------- | ------ | --------------------------- |
| `file.name`       | String | File name                   |
| `file.basename`   | String | File name without extension |
| `file.path`       | String | Full path to file           |
| `file.folder`     | String | Parent folder path          |
| `file.ext`        | String | File extension              |
| `file.size`       | Number | File size in bytes          |
| `file.ctime`      | Date   | Created time                |
| `file.mtime`      | Date   | Modified time               |
| `file.tags`       | List   | All tags in file            |
| `file.links`      | List   | Internal links in file      |
| `file.backlinks`  | List   | Files linking to this file  |
| `file.embeds`     | List   | Embeds in the note          |
| `file.properties` | Object | All frontmatter properties  |
