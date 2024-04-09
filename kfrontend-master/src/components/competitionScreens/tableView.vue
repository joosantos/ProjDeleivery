<template>
	<div>
		<SendCombatModal
			:open="openModal"
			:match="match"
			:tournament="tournament"
			:number="(match?.number_by_area || 1).toString()"
			:save-points="savePoints"
			@sent="nextMatchOrPodium"
			@close="closeModal"
			@reload="reloadMatch"
			@winner="(option) => getWinner(option)" />
		<RequestCombatNumberModal
			:open="openNumberModal"
			:number="(match?.number_by_area || 1).toString()"
			@next="nextMatch"
			@close="openNumberModal = false" />
		<ConfirmPodiumModal
			:open="openConfirmPodium && state.winner === 0"
			:tournament-id="tournament?.id"
			:number="state.nextNumber.toString()"
			@close="openConfirmPodium = false"
			@next="nextMatch"
			@show-podium="getPodium" />
		<TournamentModal
			:tournament="tournament"
			:open="showTournamentModal"
			@close="showTournamentModal = false" />
		<CallRequestModal
			:competition-id="props.competitionId"
			:number="match?.number_by_area || 1"
			:open="openCallRequest"
			:day="state.competitionDay"
			:morning="state.morning"
			@close="openCallRequest = false" />
		<!-- Loading -->
		<div v-if="loading" class="fixed inset-0 bg-gray-100 z-50 opacity-80">
			<div class="relative top-1/2 -translate-y-1/2">
				<Loading :size="10" />
			</div>
		</div>
		<div class="max-h-screen h-screen relative overflow-y-hidden bg-white mx-6">
			<!-- Header -->
			<div v-if="state.winner == 0" class="py-2 px-4">
				<div
					class="w-full text-center border-2 border-black text-3xl font-bold p-4 rounded-full bg-gray-200">
					{{ state?.title == null ? " " : state.title }}
				</div>
			</div>

			<!-- Athletes -->
			<div v-if="state.winner == 0">
				<div v-if="state.isTournament" class="overflow-hidden w-full">
					<TournamentView
						:tournament="tournament || null"
						:match-index="state.matchIndex"
						:match-number="match?.number_by_area || 1"
						:modal-open="modalOpen"
						@hide-points="
							(option) => {
								state.hidePoints = option;
								update();
							}
						"
						@hide-fouls="
							(option) => {
								state.hideFouls = option;
								update();
							}
						"
						@show-poster="
							(option) => {
								state.showPic = option;
								update();
							}
						"
						@open-call-request="openCallRequest = true"
						@day-time="(option) => (state.morning = option)"
						@number-day="(option) => (state.competitionDay = option)"
						@show-tournament="showTournamentModal = true"
						@select-match="openNumberModal = true"
						@match="
							(option) => {
								state.fight = option;
								update();
							}
						"
						@winner="
							(option) => {
								getWinner(option);
								match.winner_aux = option;
								update();
							}
						"
						@save-match="
							openModal = true;
							savePoints = false;
						"
						@save-points="
							openModal = true;
							savePoints = true;
						" />
				</div>
				<div v-else class="h-full overflow-hidden grid">
					<ListView
						:tournament="tournament || null"
						:match-index="state.matchIndex"
						:match-number="match?.number_by_area || 1"
						:modal-open="modalOpen"
						:show-podium="state.showPodium"
						@show-poster="
							(option) => {
								state.showPic = option;
								update();
							}
						"
						@show-podium="updatePodium"
						@open-call-request="openCallRequest = true"
						@day-time="(option) => (state.morning = option)"
						@number-day="(option) => (state.competitionDay = option)"
						@show-tournament="showTournamentModal = true"
						@select-match="openNumberModal = true"
						@match="
							(option) => {
								state.fight = option;
								update();
							}
						"
						@save-match="
							openModal = true;
							savePoints = false;
						" />
				</div>
			</div>

			<!-- Win Screen -->
			<div v-else class="overflow-y-auto absolute inset-0">
				<ShowWinner
					:title="state.winnerDetails.title"
					:winner-red="state.winner === 1"
					:athlete-name="state.winnerDetails.name"
					:team-name="state.winnerDetails.team"
					:match-number="state.winnerDetails.match || 1"
					@close="
						state.winner = 0;
						update();
					" />
			</div>
		</div>
	</div>
</template>

<script setup>
import ShowWinner from "@/components/competitionScreens/partials/showWinner.vue";
import TournamentView from "@/components/competitionScreens/partials/tournamentView.vue";
import ListView from "@/components/competitionScreens/partials/listView.vue";
import Loading from "@/components/partials/loading.vue";
import SendCombatModal from "@/components/competitionScreens/modals/sendCombatModal.vue";
import RequestCombatNumberModal from "@/components/competitionScreens/modals/requestCombatNumber.vue";
import ConfirmPodiumModal from "@/components/competitionScreens/modals/confirmPodium.vue";
import TournamentModal from "@/components/competitionScreens/modals/tournament.vue";
import CallRequestModal from "@/components/competitionScreens/modals/callRequest.vue";
import store from "@/store";
import { authApi } from "@/services/api";
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import toast from "@/toast.js";
import { getAthleteName, getTeamName } from "@/services/athlete.service";
import { getTournamentName } from "@/services/competition.service";

let { t } = useI18n({ useScope: "global" });

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

const props = defineProps({
	competitionId: {
		type: String,
		required: true,
	},
});

let openModal = ref(false);
let openNumberModal = ref(false);
let showTournamentModal = ref(false);
let openCallRequest = ref(false);
let loading = ref(false);
let match = ref({});
let tournament = ref({});
let definedTime = ref("00:00");
let openConfirmPodium = ref(false);
let savePoints = ref(false);
let state = ref({
	athleteRed: {
		fouls: 0,
		points: 0,
	},
	athleteBlue: {
		fouls: 0,
		points: 0,
	},
	fight: "0",
	timer: {
		seconds: 0,
		minutes: 0,
	},
	matches: [],
	isTournament: true,
	title: "",
	start: false,
	winner: 0,
	hidePoints: false,
	hideFouls: false,
	morning: true,
	competitionDay: 1,
	showPic: false,
	showPodium: true,
	podium: {
		first: "",
		second: "",
		third: "",
	},
	nextNumber: 0,
	winnerDetails: {
		name: "",
		team: "",
		title: "",
		match: 1,
	},
});

const modalOpen = computed(() => {
	return (
		openModal.value ||
		openNumberModal.value ||
		openCallRequest.value ||
		openConfirmPodium.value ||
		showTournamentModal.value
	);
});

if (localStorage.getItem("combatDetails") != null) {
	state.value = JSON.parse(localStorage.getItem("combatDetails"));
	definedTime.value = state.value.timer.minutes + ":" + state.value.timer.seconds;
	state.value.winner = 0;
}
nextMatch(state.value.fight);

function getPodium(first, second, third) {
	state.value.podium.first = first;
	state.value.podium.second = second;
	state.value.podium.third = third;
	state.value.showPodium = true;
	update();
}

function updatePodium(showPodium) {
	if (showPodium) {
		state.value.podium.first = getAthleteName(tournament.value.first_place);
		state.value.podium.second = getAthleteName(tournament.value.second_place);
		state.value.podium.third = getAthleteName(tournament.value.third_place);
	}
	state.value.showPodium = showPodium;
	update();
}

store.commit("setCombatDetails", state.value);

function update() {
	let aux = definedTime.value.split(":");
	state.value.timer.minutes = aux[0];
	state.value.timer.seconds = aux[1];
	localStorage.setItem("combatDetails", JSON.stringify(state.value));
}

function nextMatchOrPodium(number) {
	let biggestNumber = Math.max(...tournament.value.matches.map((a) => a.number_by_area));

	if (match.value.number_by_area != biggestNumber && tournament.value.first_place_id == null) {
		nextMatch(number);
		return;
	}
	state.value.nextNumber = number;
	openConfirmPodium.value = true;
}

function nextMatch(number) {
	loading.value = true;
	let nextNumber = number;
	if (number == null || number == "" || number == "0" || number == 0) {
		nextNumber = 1;
	}
	authApi
		.get(
			`matches/competition/${props.competitionId}/next?area=${store.getters.getUser.name
				.replace("Area", "")
				.trim()}&day=${
				state.value.competitionDay
			}&morning=${state.value.morning.toString()}&number=${nextNumber}`
		)
		.then((response) => {
			if (response.data == null) {
				toast.error(t("notFound.match"));
				loading.value = false;
				return;
			}
			response.data.matches.sort((a, b) => a.number > b.number);
			tournament.value = response.data;
			state.value.matches = [];
			state.value.matchIndex = 0;
			for (let mat of tournament.value.matches) {
				if (mat.number_by_area == nextNumber) {
					match.value = mat;
					state.value.matchIndex = mat.number - 1;
				}
				state.value.matches.push({
					number: mat.number,
					number_by_area: mat.number_by_area?.toString().padStart(3, "0"),
					athlete_red: getAthleteName(mat.athlete_red),
					team_red: getTeamName(mat.athlete_red),
					points_red: formatPoints(mat.points_red_total),
					athlete_blue: getAthleteName(mat.athlete_blue),
					team_blue: getTeamName(mat.athlete_blue),
					points_blue: formatPoints(mat.points_blue_total),
				});
			}
			state.value.title = getTournamentName(tournament.value, t);
			state.value.isTournament = tournament.value.category.category_type.name == "Tournament";
			if (state.value.isTournament) state.value.showPodium = false;

			match.value.winner_aux = 0;
			state.value.athleteRed.points = 0;
			state.value.athleteRed.fouls = 0;
			state.value.athleteBlue.points = 0;
			state.value.athleteBlue.fouls = 0;
			state.value.fight = match.value.number_by_area;

			update();
			loading.value = false;
		})
		.catch((error) => {
			console.error("Error Getting Next Match", error);
			toast.error("Couldn't load next match");
			loading.value = false;
		});
}

function closeModal() {
	openModal.value = false;
}

function formatPoints(points) {
	if (points == "" || points == null) {
		return "00.00";
	}
	let splited = points.toString().split(".");
	if (splited.length == 1) {
		return `${splited[0].padStart(2, "0")}.00`;
	} else {
		return `${splited[0].padStart(2, "0")}.${splited[1].padEnd(2, "0")}`;
	}
}

function reloadMatch() {
	loading.value = true;
	let matchNumber = match.value.number_by_area;
	authApi
		.get(
			`matches/competition/${
				props.competitionId
			}/next?area=${store.getters.getUser.name.replace("Area", "")}&day=${
				state.value.competitionDay
			}&morning=${state.value.morning.toString()}&number=${matchNumber}`
		)
		.then((response) => {
			if (response.data == null) {
				toast.error(t("notFound.match"));
				loading.value = false;
				return;
			}
			tournament.value = response.data;
			tournament.value.matches.sort((a, b) => a.number > b.number);
			state.value.matches = [];
			state.value.matchIndex = 0;
			for (let mat of tournament.value.matches) {
				if (mat.number_by_area == matchNumber) {
					match.value = mat;
					state.value.matchIndex = mat.number - 1;
				}
				state.value.matches.push({
					number: mat.number,
					number_by_area: mat.number_by_area?.toString().padStart(3, "0"),
					athlete_red: getAthleteName(mat.athlete_red),
					team_red: getTeamName(mat.athlete_red),
					points_red: formatPoints(mat.points_red_total),
					athlete_blue: getAthleteName(mat.athlete_blue),
					team_blue: getTeamName(mat.athlete_blue),
					points_blue: formatPoints(mat.points_blue_total),
				});
			}
			state.value.title = getTournamentName(tournament.value, t);
			state.value.isTournament = tournament.value.category.category_type.name == "Tournament";
			if (!state.value.isTournament) state.value.showPodium = false;

			match.value.winner_aux = 0;

			update();
			loading.value = false;
		})
		.catch((error) => {
			console.error("Error Getting Next Match", error);
			toast.error("Couldn't load next match");
			loading.value = false;
		});
}

function getWinner(winner_num) {
	state.value.winnerDetails = {
		name:
			winner_num === 1
				? state.value.matches[state.value.matchIndex].athlete_red
				: state.value.matches[state.value.matchIndex].athlete_blue,
		team:
			winner_num === 1
				? state.value.matches[state.value.matchIndex].team_red
				: state.value.matches[state.value.matchIndex].team_blue,

		title: state.value.title,
		match: match.value.number_by_area,
	};
	state.value.winner = winner_num;
	update();
}
</script>
