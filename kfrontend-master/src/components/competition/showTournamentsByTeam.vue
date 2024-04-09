<template>
	<div>
		<!-- Team Selector for Admin -->
		<Loading v-if="!teams.length" :size="10" />
		<form>
			<SearchSelect
				:title="t('selectTeam')"
				:options="teams"
				:option-selected="teamSelected"
				:error="''"
				@selected="
					(option) => {
						teamSelected = option;
						getTournamentsByTeam();
					}
				" />
		</form>
		<div v-if="teamSelected" class="text-lg">
			<Loading v-if="!tournamentsLoaded" :size="10" />
			<div v-else class="mt-4">
				<form>
					<CustomInput
						:type="'text'"
						:name="'athleteName'"
						:label="t('athleteName')"
						:error="''"
						:option-selected="athleteName"
						@value-changed="(option) => (athleteName = option)" />
				</form>
				<div class="grid grid-cols-6 text-center font-medium text-xl mt-4">
					<p>{{ t("name") }}</p>
					<p>{{ t("matchNumberCorner") }}</p>
					<p class="col-span-2">{{ t("category") }}</p>
					<p>{{ t("division") }}</p>
					<p>{{ t("classification") }}</p>
				</div>
				<div v-for="day of Object.keys(tournaments)" :key="day">
					<div
						v-show="tournaments[day][time].length"
						v-for="time of Object.keys(tournaments[day])"
						:key="time">
						<p class="text-3xl font-semibold text-center mt-8">
							{{
								day === "none"
									? t("withoutDay")
									: `${t("day", { day: day.substring(3, 4) })} ${t(time)}`
							}}
						</p>
						<div
							v-show="match.name.indexOf(athleteName) !== -1"
							v-for="match of tournaments[day][time]"
							:key="match"
							class="border-b border-black">
							<div class="grid grid-cols-6 text-center text-lg">
								<p>{{ match.name }}</p>
								<div class="inline-flex max-w-max mx-auto">
									<p v-if="match.area" class="text-xl">
										{{ `A${match.area}` }}
									</p>
									<div
										v-if="match.numberExists"
										:class="[
											'h-5 w-5 rounded-full border border-black mt-1 ml-1',
											match.corner === 'red' ? 'bg-red-500' : 'bg-blue-500',
										]" />
									<p class="text-xl ml-2">
										{{ match.number }}
									</p>
								</div>
								<router-link
									target="_blank"
									:to="{
										name: 'Show Tournament',
										params: { tournament: match.tournament_id },
									}"
									class="col-span-2 link">
									{{ match.category }}
								</router-link>
								<p>
									{{ match.division }}
								</p>
								<p
									v-if="match.classification"
									:class="[
										'font-medium text-xl',
										match.classification === 'firstPlace'
											? 'text-[#FFD700]'
											: match.classification === 'secondPlace'
											? 'text-[#BFBFBF]'
											: match.classification === 'thirdPlace'
											? 'text-[#CD7F32]'
											: 'text-black',
									]">
									{{ t(match.classification) }}
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { getAthleteName } from "@/services/athlete.service.js";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Loading from "@/components/partials/loading.vue";
import { authApi, errorHandling } from "@/services/api";
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });
const teams = ref([]);
const teamSelected = ref(null);
const tournamentsLoaded = ref(false);
const athleteName = ref("");
const tournaments = ref({
	none: {
		none: [],
	},
	day1: {
		morning: [],
		afternoon: [],
	},
	day2: {
		morning: [],
		afternoon: [],
	},
	day3: {
		morning: [],
		afternoon: [],
	},
});

const props = defineProps({
	// ID of the competition
	competitionId: {
		type: String,
		required: true,
	},
});

onMounted(async () => {
	try {
		const { data } = await authApi.get(`competitions/${props.competitionId}/get-teams`);
		teams.value = data.map((a) => ({ id: a.id, name: `${a.name} (${a.abbreviation})` }));
	} catch (e) {
		errorHandling(e);
	}
});

const getTournamentsByTeam = async () => {
	if (teamSelected.value == null) return;
	tournamentsLoaded.value = false;
	try {
		const { data } = await authApi.get(
			`tournaments?competition_id=${props.competitionId}&team_id=${teamSelected.value}&limit=-1`
		);
		tournaments.value = {
			none: {
				none: [],
			},
			day1: {
				morning: [],
				afternoon: [],
			},
			day2: {
				morning: [],
				afternoon: [],
			},
			day3: {
				morning: [],
				afternoon: [],
			},
		};
		for (const tournament of data.results) {
			for (const match of tournament.matches) {
				let i = 0;
				for (const athlete of [match.athlete_red, match.athlete_blue]) {
					if (
						getAthlete(athlete)?.team_id == teamSelected.value &&
						((match.number_by_area == null && tournament.day == null) ||
							(match.number_by_area != null && tournament.day != null))
					) {
						tournaments.value[tournament.day ? `day${tournament.day}` : "none"][
							tournament.day ? (tournament.morning ? "morning" : "afternoon") : "none"
						].push({
							tournament_id: tournament.id,
							corner: i === 0 ? "red" : "blue",
							name: getAthleteName(athlete) || "",
							category: tournament?.category?.name || "",
							division: getAgeAndWeight(tournament),
							area: tournament.area,
							number: formatNumber(match.number_by_area),
							numberExists: match.number_by_area != null,
							classification:
								tournament.first_place_id === athlete.id
									? "firstPlace"
									: tournament.second_place_id === athlete.id
									? "secondPlace"
									: tournament.third_place_id === athlete.id
									? "thirdPlace"
									: tournament.first_place_id == null
									? ""
									: "other",
						});
					}
					i = 1;
				}
			}
		}
		for (const day of Object.keys(tournaments.value)) {
			for (const time of Object.keys(tournaments.value[day])) {
				tournaments.value[day][time].sort((a, b) => {
					if (a.area != b.area) return Number(a.area) > Number(b.area);
					return Number(a.number) > Number(b.number);
				});
			}
		}
	} catch (e) {
		errorHandling(e);
	}
	tournamentsLoaded.value = true;
};

const getAthlete = (athleteCompetition) => {
	if (
		!athleteCompetition ||
		!athleteCompetition.athletes_group ||
		athleteCompetition.athletes_group.length === 0
	)
		return null;
	return athleteCompetition.athletes_group[0].athlete;
};

const formatNumber = (number) => {
	if (number == null) return "---------";
	return number;
	// if (number < 0) return `-${Math.abs(number).toString().padStart(2, "0")}`;
	// return number.toString().padStart(3, "0");
};

const getAgeAndWeight = (tournament) => {
	let name = "";
	if (tournament.age_min == null && tournament.age_min == null) {
		name += "";
	} else {
		if (tournament.age_min == null) {
			name += `+${tournament.age_max}`;
		} else {
			if (tournament.age_max == null) {
				name += `+${tournament.age_min}`;
			} else {
				name += `${tournament.age_min} - ${tournament.age_max}`;
			}
		}
	}

	if (!(tournament.weight_min == null && tournament.weight_max == null)) {
		if (tournament.weight_min == null) {
			name += " / -" + tournament.weight_max + "Kg";
		} else {
			if (tournament.weight_max == null) {
				name += " / +" + tournament.weight_min + "Kg";
			} else {
				name += " / " + tournament.weight_min + "/" + tournament.weight_max + "Kg.";
			}
		}
	}

	return name;
};
</script>
