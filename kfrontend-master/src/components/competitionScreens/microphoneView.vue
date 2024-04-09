<template>
	<div>
		<CallMadeModal
			:open="openModal"
			:match="matchModal"
			@close="
				openModal = false;
				matchModal = null;
			"
			@sent="callSent" />
		<CallMadeSpecialModal
			:open="openModalSpecial"
			:match="matchModal"
			@close="
				openModalSpecial = false;
				matchModal = null;
			"
			@sent="
				specials.splice(
					specials.findIndex(
						(a) => a.id == matchModal.id && a.isFireman == matchModal.isFireman
					),
					1
				)
			" />
		<Loading v-if="loading" />
		<div v-else>
			<div class="grid grid-cols-8">
				<div class="col-start-3 col-span-4">
					<!-- Refresh Button -->
					<div class="max-w-xl mx-auto">
						<div class="max-w-max">
							<Button
								:type="'primary'"
								size="small"
								:loading="showLoading"
								:message="t('refreshCallRequests', { timer: timeShow })"
								@button-click="makeCallNow()" />
						</div>
					</div>
					<!-- Special Calls -->
					<div class="inline-flex w-full justify-center">
						<div class="ml-auto mr-10">
							<div v-for="match of specials" :key="match.id" class="mt-4">
								<AmbulanceIcon
									v-if="match.isFireman"
									class="w-[4.5rem] h-[4.5rem] text-red-500" />
								<MopIcon v-else class="w-[4.5rem] h-[4.5rem] text-yellow-500" />
							</div>
						</div>
						<div class="max-w-xl my-auto space-y-4 mt-4 w-full">
							<div
								v-for="match of specials"
								:key="match.id"
								:class="[
									'px-4 py-1 cursor-pointer rounded-xl w-full space-y-2 group',
									match.isFireman
										? 'bg-red-200 hover:bg-red-300'
										: 'bg-yellow-200 hover:bg-yellow-300',
								]"
								@click="
									matchModal = match;
									openModalSpecial = true;
								">
								<p class="text-xl font-medium">
									{{ t("areaNumber", { number: match.area_to_call }) }}
								</p>
								<p class="text-lg font-medium capitalize">
									{{ t(match.isFireman ? "callFireman" : "callCleaning") }}
								</p>
							</div>
						</div>
						<div class="ml-10 mr-auto">
							<div v-for="match of specials" :key="match.id" class="mt-4">
								<AmbulanceIcon
									v-if="match.isFireman"
									class="w-[4.5rem] h-[4.5rem] text-red-500" />
								<MopIcon v-else class="w-[4.5rem] h-[4.5rem] text-yellow-500" />
							</div>
						</div>
					</div>
					<!-- Normal Calls -->
					<div class="max-w-xl space-y-4 mt-4 mx-auto">
						<CallCard
							:matches="matches"
							@open-modal="
								(option) => {
									matchModal = option;
									openModal = true;
								}
							" />
					</div>
				</div>
				<div class="col-span-2">
					<CallHistory :update="updateHistory" @updated="updateHistory = false" />
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import AmbulanceIcon from "@/components/icons/ambulance.vue";
import MopIcon from "@/components/icons/mop.vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import CallMadeSpecialModal from "@/components/competitionScreens/modals/callMadeSpecial.vue";
import CallMadeModal from "@/components/competitionScreens/modals/callMade.vue";
import CallCard from "@/components/competitionScreens/partials/callCard.vue";
import CallHistory from "@/components/competitionScreens/partials/callHistory.vue";
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { authApi } from "@/services/api";
import toast from "@/toast.js";

let { t } = useI18n({ useScope: "global" });
let matches = ref([]);
let specials = ref([]);
let loading = ref(true);
let openModal = ref(false);
let openModalSpecial = ref(false);
let matchModal = ref(null);
let promiseRequest = ref(null);
let showLoading = ref(false);
let timer = ref(0);
let timeShow = ref("15s");
let promiseTimer = ref(null);
let updateHistory = ref(false);

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
		.get(`matches/call-requests/competitions/${props.competitionId}`)
		.then((response) => {
			for (let match of response.data) {
				let index = matches.value.findIndex((a) => a.id === match.id);
				let indexFireman = specials.value.findIndex(
					(a) => a.id === match.id && a.isFireman == match.call_request_fireman
				);
				let indexClean = specials.value.findIndex(
					(a) => a.id === match.id && !a.isFireman == match.call_request_clean
				);

				if (match.call_request && index === -1) matches.value.push(match);
				if (match.call_request_fireman && indexFireman === -1) {
					match.isFireman = true;
					specials.value.push(match);
				}
				if (match.call_request_clean && indexClean === -1) {
					let aux = structuredClone(match);
					aux.isFireman = false;
					specials.value.push(aux);
				}
			}
			promiseRequest.value = setTimeout(makeCallNow, 15000);
			timer.value = 16;
			getTimer();
			promiseTimer.value = setInterval(getTimer, 1000);
			loading.value = false;
			showLoading.value = false;
		})
		.catch((error) => {
			console.error("Error Getting Matches Requests", error);
			toast.error(t("notFound.callRequests"));
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

function callSent() {
	let matchAux = matches.value.splice(
		matches.value.findIndex((a) => a.id == matchModal.value.id),
		1
	);
	if (!matchAux.length) return;
	matchAux = matchAux[0];

	let history = JSON.parse(localStorage.getItem("callHistory")) || [];

	if (history.length > 29) {
		history.splice(29, history.length);
	}
	history.push(matchAux);
	localStorage.setItem("callHistory", JSON.stringify(history));
	updateHistory.value = true;
}
</script>
