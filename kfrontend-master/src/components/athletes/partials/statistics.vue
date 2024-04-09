<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<!-- Categories form -->
		<div class="w-full space-y-2 mt-4">
			<div v-show="categories.length" class="inline-flex gap-x-2">
				<p class="text-lg font-medium">{{ t("selectCategories", 2) }}</p>
				<CategoryButton
					:name="t('selectAll')"
					:selected="false"
					@click="
						() => {
							categories = categories.map(({ show, ...rest }) => ({
								show: true,
								...rest,
							}));
							getResults();
						}
					" />
			</div>
			<div
				v-show="categories.length"
				class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-y-2 gap-x-4">
				<CategoryButton
					v-for="category of categories"
					:key="category.name"
					:name="category.name"
					:selected="category.show || false"
					@click="(category.show = !category.show), getResults()" />
			</div>
			<div
				v-show="categories.length"
				class="flex flex-col md:flex-row md:inline-flex gap-x-4 relative left-1/2 -translate-x-1/2">
				<CustomInput
					:type="'text'"
					:name="'name'"
					:mask="'###'"
					:label="t('minAge')"
					:option-selected="state.ageMin"
					:error="''"
					@value-changed="
						(option) => {
							state.ageMin = option;
							getResults();
						}
					" />
				<CustomInput
					:type="'text'"
					:name="'name'"
					:mask="'###'"
					:label="t('maxAge')"
					:option-selected="state.ageMax"
					:error="''"
					@value-changed="
						(option) => {
							state.ageMax = option;
							getResults();
						}
					" />
				<ToogleInput
					v-if="props.showPenalizations"
					:label="t('calculateResultsWithPenalizations')"
					:name="'calculateResultsWithPenalizations'"
					:option-selected="calculateWithPenalizations"
					:error="''"
					@value-changed="(option) => (calculateWithPenalizations = option)" />
			</div>
		</div>

		<!-- Penalizations -->
		<div
			v-if="
				props.showPenalizations &&
				(penalizations.results.length || store.getters.getUserRole === 'ADMIN')
			"
			class="border border-black bg-blue-200 rounded-lg w-full relative left-1/2 -translate-x-1/2 p-2 text-xl mt-4 text-center">
			<p class="font-semibold text-center">
				{{ t("penalizations") }}
			</p>

			<!-- Add penalization form -->
			<FormTemplate
				v-if="store.getters.getUserRole === 'ADMIN'"
				class="mt-4"
				:button-text="'addPenalization'"
				:loading="loadingPenalization"
				@submit-form="addPenalization"
				@clear-form="clearForm">
				<div class="grid grid-cols-1 lg:grid-cols-5 gap-x-8">
					<SearchSelect
						class="col-span-2 my-auto"
						:options="
							allTeams.map((a) => ({
								name: `${a.name} (${a.abbreviation})`,
								id: a.id,
							}))
						"
						:title="t('forms.team')"
						:option-selected="penalization.teamId"
						:error="errors.teamId ? t('error.required') : ''"
						@selected="(option) => (penalization.teamId = option)" />
					<CustomInput
						class="my-auto"
						:type="'text'"
						:name="'description'"
						:label="t('forms.pointsPenalization')"
						:error="errors.points ? t('error.invalidNumber') : ''"
						:option-selected="penalization.points"
						@value-changed="(option) => (penalization.points = option)" />
					<TextAreaInput
						class="col-span-2"
						:type="'text'"
						:name="'description'"
						:label="t('forms.description')"
						:error="errors.description ? t('error.required') : ''"
						:option-selected="penalization.description"
						@value-changed="(option) => (penalization.description = option)" />
				</div>
			</FormTemplate>

			<!-- Penalizations -->

			<Loading v-if="loadingPenalizationList" :size="10" />
			<table v-else-if="penalizations.results.length" class="table-auto w-full mt-4">
				<thead>
					<tr>
						<th>{{ t("team") }}</th>
						<th>{{ t("reason") }}</th>
						<th>{{ t("points") }}</th>
						<th v-if="store.getters.getUserRole === 'ADMIN'">{{ t("delete") }}</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="penalty of penalizations.results" :key="penalty.id">
						<td>{{ getTeam(penalty.team_id) }}</td>
						<td>{{ penalty.description }}</td>
						<td>{{ t("pointsNumber", { number: penalty.points }) }}</td>
						<td
							v-if="store.getters.getUserRole === 'ADMIN'"
							class="inline-flex gap-x-2 text-red-500 cursor-pointer hover:bg-red-200 py-0.5 px-2 rounded-full"
							@click="deletePenalization(penalty.id)">
							<XMarkIcon class="w-5 h-5 my-auto" />
							{{ t("remove") }}
						</td>
					</tr>
				</tbody>
			</table>
			<p v-else class="my-8 font-medium">{{ t("noPenalizations") }}</p>
		</div>

		<!-- Tables -->
		<div class="mt-4 flex flex-col md:flex-row w-full space-y-4 gap-x-4">
			<div class="w-full lg:w-1/2 mx-auto">
				<StatisticsTable
					class="mx-auto"
					:title="t('athlete.self', 2)"
					:results="athletes"
					:getUrl="
						({ id }) => ({
							name: 'Athlete Page',
							params: {
								athleteId: id,
							},
						})
					" />
			</div>
			<div class="w-full lg:w-1/2 mx-auto">
				<StatisticsTable
					class="mx-auto"
					:title="t('team')"
					:results="teams"
					:getUrl="
						({ id, competitionId }) => ({
							name: 'Team Statistics',
							params: {
								competition: competitionId,
								team: id,
							},
						})
					" />
			</div>
		</div>
	</div>
</template>

<script setup>
import { XMarkIcon } from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import Loading from "@/components/partials/loading.vue";
import { watch, ref } from "vue";
import toast, { genericError } from "@/toast.js";
import { unauthApi, authApi, errorHandling } from "@/services/api";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import TextAreaInput from "@/components/partials/inputs/textAreaInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import CategoryButton from "@/components/athletes/partials/categoryButton.vue";
import StatisticsTable from "@/components/athletes/partials/statisticsTable.vue";
import store from "@/store";
import { getAge } from "@/services/athlete.service";

const { t } = useI18n({ useScope: "global" });
const props = defineProps({
	url: {
		type: String,
		required: true,
	},
	before2024: {
		type: Boolean,
		required: true,
	},
	immediate: {
		type: Boolean,
		required: true,
	},
	competitionId: {
		type: String,
		required: false,
		default: "",
	},
	showPenalizations: {
		type: Boolean,
		required: false,
		default: false,
	},
});
const penalization = ref({
	teamId: "",
	points: "",
	description: "",
});
const results = ref(null);
const allTeams = ref([]);
const categories = ref([]);
const athletes = ref([]);
const teams = ref([]);
const loading = ref(props.immediate);
const loadingPenalization = ref(false);
const loadingPenalizationList = ref(true);
const penalizations = ref(null);
const calculateWithPenalizations = ref(true);
const state = ref({
	ageMin: "0",
	ageMax: "0",
});
const errors = ref({
	teamId: false,
	points: false,
	description: false,
});

watch(
	() => props.url,
	async (to, from) => {
		if (to == from) return;
		try {
			const { data } =
				store.getters.getUserRole === "ADMIN"
					? await authApi.get(to)
					: await unauthApi.get(to);
			results.value = data;
			if (props.showPenalizations) await getPenalizations();
			getCategories();
			getResults();
		} catch (e) {
			console.log(e);
			genericError();
		}
	},
	{ immediate: props.immediate }
);

watch(
	() => calculateWithPenalizations.value,
	async () => {
		getResults();
	}
);

watch(
	() => state.value.ageMin,
	() => {
		getResults();
	}
);

watch(
	() => state.value.ageMax,
	() => {
		getResults();
	}
);

const getCategories = () => {
	categories.value = [];
	if (results.value == null) return;
	for (const category of results.value.first) {
		if (categories.value.findIndex((a) => a.name === category.category_name) === -1)
			categories.value.push({ name: category.category_name, show: true });
	}
};

const getAthleteIndex = (tournament) => {
	const getAthleteName = (name) => {
		let aux = name.trim().split(" ");
		if (aux.length <= 1) return name;
		return `${aux[0]} ${aux[aux.length - 1]}`;
	};
	let athleteIndex = athletes.value.findIndex((a) => a.id === tournament.athlete_id);
	if (athleteIndex === -1) {
		athleteIndex = athletes.value.length;
		athletes.value.push({
			athlete_competition_id: tournament.athlete_competition_id,
			id: tournament.athlete_id,
			name: getAthleteName(tournament.athlete_name),
			team_id: tournament.team_id,
			team: tournament.team_name,
			abbreviation: tournament.team_abbreviation,
			birthday: tournament.athlete_birthday,
			tournamentsDirect: [],
			tournamentsFirst: [],
			tournamentsSecond: [],
			tournamentsThird: [],
			points: 0,
		});
	}
	return athleteIndex;
};

const getTeamIndex = (tournament, athlete) => {
	let indexTeam = teams.value.findIndex((a) => a.id === tournament.team_id);
	const index = allTeams.value.findIndex((a) => a.id === tournament.team_id);
	if (index === -1)
		allTeams.value.push({
			name: athlete.team,
			abbreviation: athlete.abbreviation,
			id: athlete.team_id,
		});
	if (indexTeam === -1) {
		indexTeam = teams.value.length;
		teams.value.push({
			name: athlete.team,
			abbreviation: athlete.abbreviation,
			competitionId: tournament.competition_id,
			id: athlete.team_id,
			tournamentsDirect: [],
			tournamentsFirst: [],
			tournamentsSecond: [],
			tournamentsThird: [],
			points: 0,
		});
	}
	return indexTeam;
};

const passedFilters = (tournament) => {
	const categoryIndex = categories.value.findIndex((a) => a.name === tournament.category_name);
	if (categoryIndex === -1 || !categories.value[categoryIndex].show) return false;
	const age = getAge(tournament.athlete_birthday, true, tournament.competition_start_date);
	if (Number(state.value.ageMin) != 0 && age < Number(state.value.ageMin)) return false;
	if (Number(state.value.ageMax) != 0 && age > Number(state.value.ageMax)) return false;
	return true;
};

const getResults = () => {
	if (
		isNaN(state.value.ageMin) ||
		isNaN(state.value.ageMax) ||
		Number(state.value.ageMin < 0) ||
		Number(state.value.age_max > 130)
	) {
		toast.error("Invalid values for the ages");
		return;
	}

	athletes.value = [];
	teams.value = [];
	if (props.before2024) {
		for (const tournament of results.value.first) {
			if (!passedFilters(tournament)) continue;
			const indexAthlete = getAthleteIndex(tournament);
			const indexTeam = getTeamIndex(tournament, athletes.value[indexAthlete]);

			if (
				results.value.direct.findIndex(
					(a) => a.tournament_id === tournament.tournament_id
				) === -1
			) {
				athletes.value[indexAthlete].tournamentsFirst.push(tournament.tournament_id);
				athletes.value[indexAthlete].points += 501;
				teams.value[indexTeam].tournamentsFirst.push(tournament.tournament_id);
				teams.value[indexTeam].points += 501;
			} else {
				athletes.value[indexAthlete].tournamentsDirect.push(tournament.tournament_id);
				athletes.value[indexAthlete].points += 500;
				teams.value[indexTeam].tournamentsDirect.push(tournament.tournament_id);
				teams.value[indexTeam].points += 500;
			}
		}
		for (const tournament of results.value.second) {
			if (!passedFilters(tournament)) continue;
			const indexAthlete = getAthleteIndex(tournament);
			const indexTeam = getTeamIndex(tournament, athletes.value[indexAthlete]);

			athletes.value[indexAthlete].tournamentsSecond.push(tournament.tournament_id);
			athletes.value[indexAthlete].points += 301;
			teams.value[indexTeam].tournamentsSecond.push(tournament.tournament_id);
			teams.value[indexTeam].points += 301;
		}
		for (const tournament of results.value.third) {
			if (!passedFilters(tournament)) continue;
			const indexAthlete = getAthleteIndex(tournament);
			const indexTeam = getTeamIndex(tournament, athletes.value[indexAthlete]);

			athletes.value[indexAthlete].tournamentsThird.push(tournament.tournament_id);
			athletes.value[indexAthlete].points += 101;
			teams.value[indexTeam].tournamentsThird.push(tournament.tournament_id);
			teams.value[indexTeam].points += 101;
		}
	} else {
		for (const tournament of results.value.first) {
			if (!passedFilters(tournament)) continue;
			const indexAthlete = getAthleteIndex(tournament);
			const indexTeam = getTeamIndex(tournament, athletes.value[indexAthlete]);

			if (
				results.value.direct.findIndex(
					(a) => a.tournament_id === tournament.tournament_id
				) === -1
			) {
				const points =
					tournament.category_type_name === "Tournament"
						? 500 + tournament.matches_participated_count
						: 501;

				athletes.value[indexAthlete].tournamentsFirst.push(tournament.tournament_id);
				athletes.value[indexAthlete].points += points;
				teams.value[indexTeam].tournamentsFirst.push(tournament.tournament_id);
				teams.value[indexTeam].points += points;
			} else {
				athletes.value[indexAthlete].tournamentsDirect.push(tournament.tournament_id);
				athletes.value[indexAthlete].points += 100;
				teams.value[indexTeam].tournamentsDirect.push(tournament.tournament_id);
				teams.value[indexTeam].points += 100;
			}
		}
		for (const tournament of results.value.second) {
			if (!passedFilters(tournament)) continue;
			const indexAthlete = getAthleteIndex(tournament);
			const indexTeam = getTeamIndex(tournament, athletes.value[indexAthlete]);

			const points =
				tournament.category_type_name === "Tournament"
					? 300 + tournament.matches_participated_count
					: 301;

			athletes.value[indexAthlete].tournamentsSecond.push(tournament.tournament_id);
			athletes.value[indexAthlete].points += points;
			teams.value[indexTeam].tournamentsSecond.push(tournament.tournament_id);
			teams.value[indexTeam].points += points;
		}
		for (const tournament of results.value.third) {
			if (!passedFilters(tournament)) continue;
			const indexAthlete = getAthleteIndex(tournament);
			const indexTeam = getTeamIndex(tournament, athletes.value[indexAthlete]);

			const points =
				tournament.category_type_name === "Tournament"
					? 100 + tournament.matches_participated_count
					: 101;

			athletes.value[indexAthlete].tournamentsThird.push(tournament.tournament_id);
			athletes.value[indexAthlete].points += points;
			teams.value[indexTeam].tournamentsThird.push(tournament.tournament_id);
			teams.value[indexTeam].points += points;
		}
	}

	if (props.showPenalizations && calculateWithPenalizations.value) {
		for (let team of teams.value) {
			const penalties = penalizations.value.results.filter((a) => a.team_id === team.id);
			for (const penalty of penalties) {
				team.points += penalty.points * 100;
			}
		}
	}

	athletes.value.sort((a, b) => b.points - a.points);
	teams.value.sort((a, b) => b.points - a.points);
	for (let athlete of athletes.value) {
		athlete.points = `${athlete.points}`;
		athlete.points = `${athlete.points.slice(
			0,
			athlete.points.length - 2
		)}.${athlete.points.slice(athlete.points.length - 2)}`;
	}
	for (let team of teams.value) {
		team.points = `${team.points}`;
		team.points = `${team.points.slice(0, team.points.length - 2)}.${team.points.slice(
			team.points.length - 2
		)}`;
	}
	loading.value = false;
};

const clearForm = () => {
	penalization.value.teamId = "";
	penalization.value.points = "";
	penalization.value.description = "";
	errors.value.teamId = false;
	errors.value.points = false;
	errors.value.description = false;
};

const addPenalization = async () => {
	errors.value.teamId = false;
	errors.value.points = false;
	errors.value.description = false;
	let number = 0;
	let description = penalization.value.description.trim();
	errors.value.description = description === "";
	errors.value.teamId = penalization.value.teamId === "";
	try {
		if (penalization.value.points === 0 || penalization.value.points === "")
			throw new Error("Invalid number");
		number = Number(penalization.value.points);
	} catch {
		errors.value.points = true;
	}
	if (errors.value.teamId || errors.value.points || errors.value.description) return;

	loadingPenalization.value = true;

	try {
		const penalty = await authApi.post("penalizations", {
			competition_id: props.competitionId,
			points: number,
			team_id: penalization.value.teamId,
			description: penalization.value.description,
		});
		await getPenalizations();
		getResults();
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingPenalization.value = false;
	}
};

const getPenalizations = async () => {
	loadingPenalizationList.value = true;
	try {
		const url = `penalizations?competition_id=${props.competitionId}&skip=0&limit=-1`;
		const { data } =
			store.getters.getUserRole === "ADMIN"
				? await authApi.get(url)
				: await unauthApi.get(url);
		penalizations.value = data;
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingPenalizationList.value = false;
	}
};

const getTeam = (teamId) => {
	const index = allTeams.value.findIndex((a) => a.id === teamId);
	if (index === -1) return t("teamNotFound");
	else return `${allTeams.value[index].name} (${allTeams.value[index].abbreviation})`;
};

const deletePenalization = async (id) => {
	loadingPenalizationList.value = true;
	try {
		await authApi.delete(`penalizations/${id}`);
		await getPenalizations();
		getResults();
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingPenalizationList.value = false;
	}
};
</script>
