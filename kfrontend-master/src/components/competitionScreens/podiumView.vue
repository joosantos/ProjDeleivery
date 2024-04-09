<template>
	<div>
		<TournamentPrintedModal
			:open="openModal"
			:tournament-id="tournamentModalId"
			:tournament-name="tournamentModalName"
			@close="
				openModal = false;
				tournamentModalId = '';
				tournamentModalName = '';
			"
			@sent="
				tournaments.splice(
					tournaments.findIndex((a) => a.id == tournamentModalId),
					1
				)
			" />
		<Loading v-if="loading" />
		<div v-else>
			<div class="max-w-xl mx-auto">
				<div class="max-w-max">
					<Button
						:type="'primary'"
						size="small"
						:loading="showLoading"
						:message="t('refreshTournaments', { timer: timeShow })"
						@button-click="makeCallNow()" />
				</div>
			</div>
			<div class="max-w-xl space-y-4 mt-4 mx-auto">
				<div
					v-for="tournament of tournaments"
					:key="tournament.id"
					class="px-4 py-2 pb-4 bg-blue-100 hover:bg-blue-200 cursor-pointer rounded-xl w-full space-y-2 group"
					@click="
						tournamentModalId = tournament.id;
						tournamentModalName = getTournamentName(tournament, t);
						openModal = true;
					">
					<p class="text-xl font-medium text-center">
						{{ getTournamentName(tournament, t) }}
					</p>
					<div class="inline-flex justify-between w-full">
						<p class="px-2 py-1 text-black">
							{{ t("areaNumber", { number: tournament.area }) }}
						</p>
						<Button
							class="max-w-max"
							:type="'primary'"
							size="small"
							:message="t('printDiplomas')"
							@button-click="printDiplomas(tournament)" />
					</div>
					<p v-if="tournament.first_place_id" class="px-2 py-1 bg-[#FFD700] rounded">
						{{ `1º- ${getAthleteNameTeam(tournament.first_place)}` }}
					</p>
					<p v-if="tournament.second_place_id" class="px-2 py-1 bg-[#BFBFBF] rounded">
						{{ `2º- ${getAthleteNameTeam(tournament.second_place)}` }}
					</p>
					<p v-if="tournament.third_place_id" class="px-2 py-1 bg-[#CD7F32] rounded">
						{{ `3º- ${getAthleteNameTeam(tournament.third_place)}` }}
					</p>
					<div v-if="tournament.podium_notes">
						<p>{{ t("notes.self", 2) }}</p>
						<p
							class="bg-yellow-500 group-hover:bg-blue-100 rounded ml-4 px-2 py-0.5 whitespace-pre-line">
							{{ tournament.podium_notes || t("notes.no") }}
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import TournamentPrintedModal from "@/components/competitionScreens/modals/tournamentPrinted.vue";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { authApi } from "@/services/api";
import toast from "@/toast.js";
import router from "@/router";
import { getAthleteNameTeam } from "@/services/athlete.service";
import { getTournamentName } from "@/services/competition.service";

let { t } = useI18n({ useScope: "global" });
let tournaments = ref([]);
let loading = ref(true);
let openModal = ref(false);
let tournamentModalId = ref("");
let tournamentModalName = ref("");
let promiseRequest = ref(null);
let showLoading = ref(false);
let timer = ref(0);
let timeShow = ref("30s");
let promiseTimer = ref(null);

const props = defineProps({
	competitionId: {
		type: String,
		required: true,
	},
});
getCallRequests();
function getCallRequests() {
	showLoading.value = true;
	authApi
		.get(`tournaments/competitions/${props.competitionId}/print-podium`)
		.then((response) => {
			for (let tournament of response.data) {
				let index = tournaments.value.findIndex((a) => a.id === tournament.id);
				if (index === -1) tournaments.value.push(tournament);
				else tournaments.value[index] = tournament;
			}
			promiseRequest.value = setTimeout(makeCallNow, 30000);
			timer.value = 31;
			getTimer();
			promiseTimer.value = setInterval(getTimer, 1000);
			loading.value = false;
			showLoading.value = false;
		})
		.catch((error) => {
			console.error("Error Getting Tournaments", error);
			toast.error(t("notFound.tournament", 2));
			loading.value = false;
			showLoading.value = false;
		});
}

function makeCallNow() {
	clearInterval(promiseRequest.value);
	clearInterval(promiseTimer.value);
	getCallRequests();
}

function getTimer() {
	if (timer.value > 0) timer.value -= 1;
	timeShow.value = `${timer.value.toString().padStart(2, "0")}s`;
}

function printDiplomas(tournament) {
	if (tournament.first_place_id != null) {
		let routeData = router.resolve({
			name: "Diploma 1",
			params: { tournament: tournament.id },
		});
		window.open(routeData.href, "_blank");
	}
}
</script>
