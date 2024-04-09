/**
 * Returns obj from .csv file
 * @returns {array}
 */
function importFromCsv(data, start_line) {
	let lines = data.split("\n");
	let aux = lines[0].split(";");
	let keys = [];
	for (let key of aux) {
		keys.push(key.replace("\r", ""));
	}
	lines.shift();
	let array = [];
	lines = lines.splice(start_line - 1, lines.length);
	for (let line of lines) {
		let lineSplited = line.split(";");
		let obj = {};
		for (let i = 0; i < lineSplited.length; i++) {
			obj[keys[i]] = lineSplited[i].replace("\r", "");
		}

		array.push(obj);
	}

	return { array: array, keys: keys };
}
export { importFromCsv };
