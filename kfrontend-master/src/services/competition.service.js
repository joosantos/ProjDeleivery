import { getAthleteNameTeam } from "@/services/athlete.service.js";

export { getPodiumNames, getHighestPlace, getHighestTeam, getTournamentName, getPodiumBracket3 };

/**
 * @param  {Object} tournament Tournament Object
 * @return {Array} Array with objects with the format {name: "", id: "", team: "", abr: "", teamId: ""} of the podium, if empty then it wasn't yet possible to get the podium ( The name of the athlete already includes the team)
 */
const getPodiumNames = function (tournament) {
	let winners = [];
	if (tournament.matches.length == 1) {
		let match = tournament.matches[0];
		if (match.winner_id == null) {
			return [];
		}
		winners.push({
			name: getAthleteNameTeam(match.winner),
			id: match.winner_id,
			teamId: match.winner.athlete.team.id,
			team: match.winner.athlete.team.name,
			abr: match.winner.athlete.team.abbreviation,
		});
		if (match.athlete_red_id != null && match.athlete_blue_id != null) {
			if (match.athlete_red_id == match.winner_id) {
				winners.push({
					name: getAthleteNameTeam(match.athlete_blue),
					id: match.athlete_blue_id,
					teamId: match.athlete_blue.athlete.team.id,
					team: match.athlete_blue.athlete.team.name,
					abr: match.athlete_blue.athlete.team.abbreviation,
				});
			} else {
				winners.push({
					name: getAthleteNameTeam(match.athlete_red),
					id: match.athlete_red,
					teamId: match.athlete_red.athlete.team.id,
					team: match.athlete_red.athlete.team.name,
					abr: match.athlete_red.athlete.team.abbreviation,
				});
			}
		}
		return winners;
	}

	if (tournament.matches.length == 3) {
		return getPodiumBracket3(tournament);
	}

	let matchFinal = null;
	let matchThird = null;
	let length = tournament.matches.length;
	for (let match of tournament.matches) {
		if (match.number == length - 1) {
			matchFinal = match;
		}
		if (match.number == length) {
			matchThird = match;
		}
	}

	if (
		matchFinal?.winner_id == null ||
		matchThird?.winner_id == null ||
		matchFinal.athlete_red_id == null ||
		matchFinal.athlete_blue_id == null ||
		matchThird.athlete_red_id == null ||
		matchThird.athlete_blue_id == null
	) {
		return [];
	}

	winners.push({
		name: getAthleteNameTeam(matchFinal.winner),
		id: matchFinal.winner_id,
		teamId: matchFinal.winner.athlete.team.id,
		team: matchFinal.winner.athlete.team.name,
		abr: matchFinal.winner.athlete.team.abbreviation,
	});
	if (matchFinal.athlete_red_id == matchFinal.winner_id) {
		winners.push({
			name: getAthleteNameTeam(matchFinal.athlete_blue),
			id: matchFinal.athlete_blue_id,
			teamId: matchFinal.athlete_blue.athlete.team.id,
			team: matchFinal.athlete_blue.athlete.team.name,
			abr: matchFinal.athlete_blue.athlete.team.abbreviation,
		});
	} else {
		winners.push({
			name: getAthleteNameTeam(matchFinal.athlete_red),
			id: matchFinal.athlete_red_id,
			teamId: matchFinal.athlete_red.athlete.team.id,
			team: matchFinal.athlete_red.athlete.team.name,
			abr: matchFinal.athlete_red.athlete.team.abbreviation,
		});
	}

	winners.push({
		name: getAthleteNameTeam(matchThird.winner),
		id: matchThird.winner_id,
		teamId: matchThird.winner.athlete.team.id,
		team: matchThird.winner.athlete.team.name,
		abr: matchThird.winner.athlete.team.abbreviation,
	});
	return winners;
};

/**
 * @param  {Object} tournament Tournament Object
 * @param  {String} athleteId Id of the athlete to find
 * @return {Number} 1, 2, 3 depending of the place of the athlete, 4 if other place than the podium, 0 if winners are not yet defined or -1 if athlete not found or an error ocurred
 */
const getHighestPlace = function (tournament, athleteId) {
	let existsFlag = false;
	let matchFinal = null;
	let matchThird = null;
	for (let match of tournament.matches) {
		if (match.athlete_red_id == athleteId || match.athlete_blue_id == athleteId) {
			existsFlag = true;
		}
		if (match.number == tournament.matches.length - 1) {
			matchFinal = match;
		}
		if (match.number == tournament.matches.length) {
			matchThird = match;
		}
	}
	if (!existsFlag) {
		return -1;
	}
	if (tournament.matches.length == 1) {
		let match = tournament.matches[0];
		if (match.winner_id == null) {
			return 0;
		}
		if (match.winner_id == athleteId) {
			return 1;
		} else {
			return 2;
		}
	}

	if (tournament.matches.length == 3) {
		let athletes = getPodiumBracket3(tournament);
		if (athletes.length < 3) {
			return 0;
		}
		if (athleteId == athletes[0].id) {
			return 1;
		}
		if (athleteId == athletes[1].id) {
			return 2;
		}
		if (athleteId == athletes[2].id) {
			return 3;
		}
		// An error ocurred
		return -1;
	}

	if (matchFinal?.winner_id == null || matchThird?.winner_id == null) {
		return 0;
	}

	if (matchFinal.winner_id == athleteId) {
		return 1;
	}
	if (matchThird.winner_id == athleteId) {
		return 3;
	}
	if (matchFinal.athlete_red_id == matchFinal.winner_id) {
		if (athleteId == matchFinal.athlete_blue_id) {
			return 2;
		}
		return 4;
	} else {
		if (athleteId == matchFinal.athlete_red_id) {
			return 2;
		}
		return 4;
	}
};

/**
 * @param  {Object} tournament Tournament Object
 * @param  {String} teamId Id of the athlete to find
 * @return {Number} 1, 2, 3 depending of the place of the athlete, 4 if other place than the podium, 0 if winners are not yet defined or -1 if athlete not found or an error ocurred
 */
const getHighestTeam = function (tournament, teamId) {
	let existsFlag = false;
	let matchFinal = null;
	let matchThird = null;
	for (let match of tournament.matches) {
		if (
			match.athlete_red?.athlete?.team?.id == teamId ||
			match.athlete_blue?.athlete?.team?.id == teamId
		) {
			existsFlag = true;
		}
		if (match.number == tournament.matches.length - 1) {
			matchFinal = match;
		}
		if (match.number == tournament.matches.length) {
			matchThird = match;
		}
	}
	if (!existsFlag) {
		return -1;
	}
	if (tournament.matches.length == 1) {
		let match = tournament.matches[0];
		if (match.winner_id == null) {
			return 0;
		}
		if (match.winner.athlete.team.id == teamId) {
			return 1;
		} else {
			return 2;
		}
	}

	if (tournament.matches.length == 3) {
		let athletes = getPodiumBracket3(tournament);
		if (athletes.length < 3) {
			return 0;
		}
		if (teamId == athletes[0].teamId) {
			return 1;
		}
		if (teamId == athletes[1].teamId) {
			return 2;
		}
		if (teamId == athletes[2].teamId) {
			return 3;
		}
		// An error ocurred
		return -1;
	}

	if (matchFinal?.winner_id == null || matchThird?.winner_id == null) {
		return 0;
	}

	if (matchFinal.winner.athlete.team.id == teamId) {
		return 1;
	}
	if (matchThird.winner.athlete.team.id == teamId) {
		return 3;
	}
	if (matchFinal.athlete_red_id == matchFinal.winner_id) {
		if (teamId == matchFinal.athlete_blue.athlete.team.id) {
			return 2;
		}
		return 4;
	} else {
		if (teamId == matchFinal.athlete_red.athlete.team.id) {
			return 2;
		}
		return 4;
	}
};

const getPodiumBracket3 = function (tournament) {
	let match3 = null;
	let match2 = null;
	for (let match of tournament.matches) {
		if (match.number == 2) {
			match2 = match;
		}
		if (match.number == 3) {
			match3 = match;
		}
	}
	if (match3?.winner_id == null || match2 == null) {
		return [];
	}

	let athlete1 = {
		name: getAthleteNameTeam(match3.athlete_red),
		id: match3.athlete_red_id,
		teamId: match3.athlete_red.athlete.team.id,
		team: match3.athlete_red.athlete.team.name,
		abr: match3.athlete_red.athlete.team.abbreviation,
		wins: 0,
		points: 0,
		secondPoints: 0,
	};
	let athlete2 = {
		name: getAthleteNameTeam(match3.athlete_blue),
		id: match3.athlete_blue_id,
		teamId: match3.athlete_blue.athlete.team.id,
		team: match3.athlete_blue.athlete.team.name,
		abr: match3.athlete_blue.athlete.team.abbreviation,
		wins: 0,
		points: 0,
		secondPoints: 0,
	};
	let athlete3 = { name: "", id: null, wins: 0, points: 0, secondPoints: 0 };
	if (
		match2.athlete_red_id != match3.athlete_red_id &&
		match2.athlete_red_id != match3.athlete_red_id
	) {
		athlete3.name = getAthleteNameTeam(match2.athlete_red);
		athlete3.id = match2.athlete_red_id;
		athlete3.team = match2.athlete_red.athlete.team.name;
		athlete3.teamId = match2.athlete_red.athlete.team.id;
		athlete3.abr = match2.athlete_red.athlete.team.abbreviation;
	} else {
		athlete3.name = getAthleteNameTeam(match2.athlete_blue);
		athlete3.id = match2.athlete_blue_id;
		athlete3.team = match2.athlete_blue.athlete.team.name;
		athlete3.teamId = match2.athlete_blue.athlete.team.id;
		athlete3.abr = match2.athlete_blue.athlete.team.abbreviation;
	}

	let winFlag = false;

	let athletes = [athlete1, athlete2, athlete3];

	for (let match of tournament.matches) {
		for (let ath of athletes) {
			if (ath.id == match.winner_id) {
				ath.wins += 1;
				if (ath.wins == 2) {
					winFlag = true;
				}
			}
			if (ath.id == match.athlete_red_id) {
				ath.points += match.points_red_total;
				ath.secondPoints +=
					match.points_red_central_referee_round2 +
					match.points_red_judge1_round2 +
					match.points_red_judge2_round2;
			}
			if (ath.id == match.athlete_blue_id) {
				ath.points += match.points_blue_total;
				ath.secondPoints +=
					match.points_blue_central_referee_round2 +
					match.points_blue_judge1_round2 +
					match.points_blue_judge2_round2;
			}
		}
	}

	if (winFlag) {
		athletes.sort((a, b) => b.wins - a.wins);
		return [athletes[0], athletes[1], athletes[2]];
	}

	athletes.sort((a, b) => {
		if (a.points == b.points) {
			return b.secondPoints - a.secondPoints;
		} else {
			return b.points - a.points;
		}
	});

	return [
		{
			name: athletes[0].name,
			id: athletes[0].id,
			team: athletes[0].team,
			teamId: athletes[0].teamId,
			abr: athletes[0].abr,
		},
		{
			name: athletes[1].name,
			id: athletes[1].id,
			team: athletes[1].team,
			teamId: athletes[1].teamId,
			abr: athletes[1].abr,
		},
		{
			name: athletes[2].name,
			id: athletes[2].id,
			team: athletes[2].team,
			teamId: athletes[2].teamId,
			abr: athletes[2].abr,
		},
	];
};

const getTournamentName = function (tournament, t) {
	let name =
		tournament.category.name +
		(tournament.is_male == null
			? ` | ${t("open")}`
			: " | " + (tournament.is_male ? t("masc") : t("fem")));

	if (tournament.age_min == null && tournament.age_min == null) {
		name += "";
	} else {
		if (tournament.age_min == null) {
			name +=
				" | -" +
				tournament.age_max +
				` ${t("year", tournament.age_max, { count: tournament.age_max })}`;
		} else {
			if (tournament.age_max == null) {
				name += " | +" + `${t("year", tournament.age_min, { count: tournament.age_min })}`;
			} else {
				name +=
					" | " +
					tournament.age_min +
					"-" +
					`${t("year", tournament.age_max, { count: tournament.age_max })}`;
			}
		}
	}

	if (!(tournament.weight_min == null && tournament.weight_max == null)) {
		if (tournament.weight_min == null) {
			name += " | -" + tournament.weight_max + " Kg";
		} else {
			if (tournament.weight_max == null) {
				name += " | +" + tournament.weight_min + " Kg";
			} else {
				name += " | " + tournament.weight_min + "/" + tournament.weight_max + " Kg.";
			}
		}
	}

	if (tournament.belt_min_id && tournament.belt_max_id) {
		if (tournament.belt_min_id == tournament.belt_max_id)
			name += ` | ${t(`belts.${tournament.belt_min.name}`)}`;
		else
			name += ` | ${t(`belts.${tournament.belt_min.name}`)} - ${t(
				`belts.${tournament.belt_max.name}`
			)}`;
	}

	return name;
};
