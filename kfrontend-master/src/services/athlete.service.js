export { getAthleteName, getAthleteNameTeam, getTeamName, getAthletesNameFromArray, getAge };

const getAthleteNameTeam = function (athlete) {
	if (athlete?.athletes_group == null || athlete.athletes_group.length == 0) {
		return null;
	}
	let team =
		athlete.athletes_group[0].athlete?.team?.abbreviation == null
			? ""
			: athlete.athletes_group[0].athlete.team.abbreviation.trim();
	return `${getAthleteName(athlete)} (${team})`;
};

const getAthleteName = (athlete) => {
	if (athlete?.athletes_group == null || athlete.athletes_group.length == 0) {
		return null;
	}
	let name = "";
	for (let group of athlete.athletes_group) {
		let nameAux = group.athlete.name.trim().split(" ");
		if (nameAux.length == 1) {
			name += `${nameAux[0]}, `;
		} else {
			name += `${nameAux[0]} ${nameAux[nameAux.length - 1]}, `;
		}
	}
	return name.slice(0, name.length - 2);
};

const getTeamName = function (athlete) {
	if (athlete == null || athlete.athletes_group.length == 0) {
		return null;
	}
	return athlete.athletes_group[0].athlete.team.abbreviation;
};

const getAthletesNameFromArray = function (athletes) {
	if (athletes == null || athletes.length == 0) {
		return "";
	}
	let name = "";
	for (let athlete of athletes) {
		let nameAux = athlete.name.trim().split(" ");
		if (nameAux.length == 1) {
			name += `${nameAux[0]}, `;
		} else {
			name += `${nameAux[0]} ${nameAux[nameAux.length - 1]}, `;
		}
	}
	return name.slice(0, name.length - 2);
};

const getAge = (birthday, calculateAtStartOfYear, dateToCalculateAgeAt) => {
	const birthDate = new Date(birthday);
	const otherDate = new Date(dateToCalculateAgeAt);
	const dateStartYear = new Date(otherDate.getFullYear(), 0, 1);

	if (calculateAtStartOfYear) return dateStartYear.getFullYear() - birthDate.getFullYear();

	let age = otherDate.getFullYear() - birthDate.getFullYear();
	if (
		otherDate.getMonth() < birthDate.getMonth() ||
		(otherDate.getMonth() == birthDate.getMonth() && otherDate.getDate() < birthDate.getDate())
	) {
		age--;
	}

	return age;
};
