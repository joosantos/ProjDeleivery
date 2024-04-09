<template>
	<TransitionRoot as="template" :show="open">
		<Dialog as="div" class="fixed z-20 inset-0 overflow-y-auto" @close="emit('close')">
			<div
				class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
				<TransitionChild
					as="template"
					enter="ease-out duration-300"
					enter-from="opacity-0"
					enter-to="opacity-100"
					leave="ease-in duration-200"
					leave-from="opacity-100"
					leave-to="opacity-0">
					<DialogOverlay
						class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
				</TransitionChild>

				<!-- This element is to trick the browser into centering the modal contents. -->
				<span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true"
					>&#8203;</span
				>
				<TransitionChild
					as="template"
					enter="ease-out duration-300"
					enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
					enter-to="opacity-100 translate-y-0 sm:scale-100"
					leave="ease-in duration-200"
					leave-from="opacity-100 translate-y-0 sm:scale-100"
					leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
					<div
						:class="[
							'inline-block align-bottom bg-gray-100 rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:w-full sm:p-6',
							isTournament ? 'sm:max-w-5xl' : 'sm:max-w-lg',
						]">
						<div>
							<!-- Referees names -->
							<div
								v-if="!savePoints"
								class="bg-white border border-black p-2 rounded-lg pb-4 px-4">
								<p class="text-center text-lg font-medium">
									{{ t("insertRefereesNames") }}
								</p>
								<div class="mx-auto my-4 max-w-max">
									<ToogleInput
										:name="'defaultFedereesNames'"
										:label="t('saveAsDefault')"
										:option-selected="saveAsDefault"
										:error="''"
										@value-changed="(option) => (saveAsDefault = option)" />
								</div>
								<div
									:class="[
										'w-full',
										isTournament ? 'space-x-5 inline-flex' : 'space-y-2',
									]">
									<div class="w-full">
										<CustomInput
											type="text"
											name="Judge1"
											:label="t('judge', { number: 1 })"
											:option-selected="state.judge1.name"
											error=""
											@value-changed="
												(option) => {
													state.judge1.name = option;
												}
											" />
									</div>
									<div class="w-full">
										<CustomInput
											type="text"
											name="central"
											:label="t('centralReferee')"
											:option-selected="state.central.name"
											error=""
											@value-changed="
												(option) => {
													state.central.name = option;
												}
											" />
									</div>
									<div class="w-full">
										<CustomInput
											type="text"
											name="Judge 2"
											:label="t('judge', { number: 2 })"
											:option-selected="state.judge2.name"
											error=""
											@value-changed="
												(option) => {
													state.judge2.name = option;
												}
											" />
									</div>
								</div>
							</div>

							<p v-if="props.savePoints" class="text-center text-3xl font-semibold">
								{{ t("savePoints") }}
							</p>

							<!-- Points -->
							<div class="inline-flex w-full gap-x-4">
								<!-- Points for Red Side -->
								<div class="mt-4 bg-red-500 rounded px-4 pt-2 pb-4 w-full">
									<p class="text-center font-medium text-lg">
										{{
											t("pointsFor", {
												name: getAthleteNameTeam(props.match?.athlete_red),
											})
										}}
									</p>

									<div class="inline-flex space-x-8 w-full">
										<div class="w-full">
											<p
												v-if="props.tournament.category.rounds"
												class="text-center font-medium">
												{{ t("round", { number: 1 }) }}
											</p>
											<div class="space-y-2">
												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge1red1"
													:label-black="true"
													:border-black="true"
													:label="t('judge', { number: 1 })"
													:option-selected="
														state.judge1.round1.athleteRed.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge1.round1.athleteRed = option;
														}
													" />

												<CustomInput
													type="text"
													name="Centralred1"
													:label="t('centralReferee')"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.central.round1.athleteRed.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.central.round1.athleteRed =
																option;
														}
													" />

												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge2red1"
													:label="t('judge', { number: 2 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge2.round1.athleteRed.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge2.round1.athleteRed = option;
														}
													" />
											</div>
										</div>
										<div v-if="props.tournament.category.rounds" class="w-full">
											<p class="text-center font-medium">
												{{ t("round", { number: 2 }) }}
											</p>
											<div class="space-y-2">
												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge1red2"
													:label="t('judge', { number: 1 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge1.round2.athleteRed.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge1.round2.athleteRed = option;
														}
													" />

												<CustomInput
													type="text"
													name="Centralred2"
													:label="t('centralReferee')"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.central.round2.athleteRed.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.central.round2.athleteRed =
																option;
														}
													" />

												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge2red2"
													:label="t('judge', { number: 2 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge2.round2.athleteRed.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge2.round2.athleteRed = option;
														}
													" />
											</div>
										</div>
									</div>
									<div class="w-full">
										<div
											v-if="props.tournament.category.rounds"
											class="inline-flex mt-4 gap-x-8 w-full">
											<CustomInput
												type="text"
												name="totalRound1"
												:label="t('totalRound', { number: 1 })"
												:label-black="true"
												:border-black="true"
												:disabled="true"
												:capitalize="true"
												:size-text="'large'"
												:option-selected="
													(
														(getNum(state.judge1.round1.athleteRed) ||
															0) +
														(getNum(state.central.round1.athleteRed) ||
															0) +
														(getNum(state.judge2.round1.athleteRed) ||
															0)
													).toString()
												"
												error=""
												@value-changed="null" />
											<CustomInput
												type="text"
												name="totalRound2"
												:label="t('totalRound', { number: 2 })"
												:label-black="true"
												:border-black="true"
												:disabled="true"
												:capitalize="true"
												:size-text="'large'"
												:option-selected="
													(
														(getNum(state.judge1.round2.athleteRed) ||
															0) +
														(getNum(state.central.round2.athleteRed) ||
															0) +
														(getNum(state.judge2.round2.athleteRed) ||
															0)
													).toString()
												"
												error=""
												@value-changed="null" />
										</div>
										<div class="mt-4 w-1/2 mx-auto">
											<CustomInput
												v-if="
													props.tournament.category.rounds ||
													props.tournament.category.three_points
												"
												type="text"
												name="total"
												:label="t('total')"
												:label-black="true"
												:border-black="true"
												:disabled="true"
												:size-text="'large'"
												:option-selected="
													(
														(getNum(state.judge1.round1.athleteRed) ||
															0) +
														(getNum(state.central.round1.athleteRed) ||
															0) +
														(getNum(state.judge2.round1.athleteRed) ||
															0) +
														(getNum(state.judge1.round2.athleteRed) ||
															0) +
														(getNum(state.central.round2.athleteRed) ||
															0) +
														(getNum(state.judge2.round2.athleteRed) ||
															0)
													).toString()
												"
												error=""
												@value-changed="null" />
										</div>
									</div>
								</div>
								<!-- Points for Blue Side -->
								<div
									v-if="
										props.tournament.category.category_type.name == 'Tournament'
									"
									class="mt-4 bg-blue-500 rounded px-4 pt-2 pb-4 w-full">
									<p class="text-center font-medium text-lg">
										{{
											t("pointsFor", {
												name: getAthleteNameTeam(props.match.athlete_blue),
											})
										}}
									</p>

									<div class="inline-flex space-x-8 w-full">
										<div class="w-full">
											<p
												v-if="props.tournament.category.rounds"
												class="text-center font-medium">
												{{ t("round", { number: 1 }) }}
											</p>
											<div class="space-y-2">
												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge1blue1"
													:label="t('judge', { number: 1 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge1.round1.athleteBlue.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge1.round1.athleteBlue =
																option;
														}
													" />

												<CustomInput
													type="text"
													name="Centralblue1"
													:label="t('centralReferee')"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.central.round1.athleteBlue.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.central.round1.athleteBlue =
																option;
														}
													" />

												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge2blue1"
													:label="t('judge', { number: 2 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge2.round1.athleteBlue.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge2.round1.athleteBlue =
																option;
														}
													" />
											</div>
										</div>
										<div v-if="props.tournament.category.rounds" class="w-full">
											<p class="text-center font-medium">
												{{ t("round", { number: 2 }) }}
											</p>
											<div class="space-y-2">
												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge1blue2"
													:label="t('judge', { number: 2 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge1.round2.athleteBlue.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge1.round2.athleteBlue =
																option;
														}
													" />

												<CustomInput
													type="text"
													name="Centralblue2"
													:label="t('centralReferee')"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.central.round2.athleteBlue.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.central.round2.athleteBlue =
																option;
														}
													" />

												<CustomInput
													v-if="props.tournament.category.three_points"
													type="text"
													name="Judge2blue2"
													:label="t('judge', { number: 2 })"
													:label-black="true"
													:border-black="true"
													:option-selected="
														state.judge2.round2.athleteBlue.toString()
													"
													error=""
													@value-changed="
														(option) => {
															state.judge2.round2.athleteBlue =
																option;
														}
													" />
											</div>
										</div>
									</div>
									<div class="w-full">
										<div
											v-if="props.tournament.category.rounds"
											class="inline-flex mt-4 gap-x-8 w-full">
											<CustomInput
												type="text"
												name="totalRound1"
												:label="t('totalRound', { number: 1 })"
												:label-black="true"
												:border-black="true"
												:disabled="true"
												:capitalize="true"
												:size-text="'large'"
												:option-selected="
													(
														(getNum(state.judge1.round1.athleteBlue) ||
															0) +
														(getNum(state.central.round1.athleteBlue) ||
															0) +
														(getNum(state.judge2.round1.athleteBlue) ||
															0)
													).toString()
												"
												error=""
												@value-changed="null" />
											<CustomInput
												type="text"
												name="totalRound2"
												:label="t('totalRound', { number: 2 })"
												:label-black="true"
												:border-black="true"
												:disabled="true"
												:capitalize="true"
												:size-text="'large'"
												:option-selected="
													(
														(getNum(state.judge1.round2.athleteBlue) ||
															0) +
														(getNum(state.central.round2.athleteBlue) ||
															0) +
														(getNum(state.judge2.round2.athleteBlue) ||
															0)
													).toString()
												"
												error=""
												@value-changed="null" />
										</div>
										<div class="mt-4 w-1/2 mx-auto">
											<CustomInput
												v-if="
													props.tournament.category.rounds ||
													props.tournament.category.three_points
												"
												type="text"
												name="total"
												:label="t('total')"
												:label-black="true"
												:border-black="true"
												:disabled="true"
												:size-text="'large'"
												:option-selected="
													(
														(getNum(state.judge1.round1.athleteBlue) ||
															0) +
														(getNum(state.central.round1.athleteBlue) ||
															0) +
														(getNum(state.judge2.round1.athleteBlue) ||
															0) +
														(getNum(state.judge1.round2.athleteBlue) ||
															0) +
														(getNum(state.central.round2.athleteBlue) ||
															0) +
														(getNum(state.judge2.round2.athleteBlue) ||
															0)
													).toString()
												"
												error=""
												@value-changed="null" />
										</div>
									</div>
								</div>
							</div>

							<!-- Save Points -->
							<div v-if="props.savePoints" class="relative mt-4">
								<Button
									:message="t('savePoints')"
									:loading="loading"
									:capitalize="true"
									type="success"
									@button-click="sendPoints" />
							</div>

							<!-- Type of Match Ending -->
							<div v-if="!props.savePoints" class="mt-4">
								<p class="text-center font-medium text-lg capitalize">
									{{ t("endType") }}
								</p>
								<div class="max-w-max mx-auto">
									<RadioGroup
										:name="'endType'"
										:label="''"
										:radio-options="endTypes"
										:columns="isTournament ? 4 : 2"
										:option-selected="state.endType"
										:error="''"
										@selected="(option) => (state.endType = option)" />
								</div>
							</div>

							<!-- Number of Next Match -->
							<div v-if="!props.savePoints" class="mt-8">
								<CustomInput
									:label="t('nextMatchNumber')"
									type="text"
									:name="'number'"
									:option-selected="state.number"
									:error="''"
									@value-changed="(option) => (state.number = option)" />
							</div>

							<!-- Send Button -->
							<div
								v-if="!props.savePoints && isTournament"
								class="inline-flex w-full gap-x-4 mt-4">
								<Button
									:class="[
										disableNumber === 2 &&
											loading &&
											'opacity-50 pointer-events-none',
									]"
									:message="
										t('saveMatchRedWinner', {
											name: getAthleteNameTeam(props.match?.athlete_red),
										})
									"
									:loading="disableNumber === 1 ? loading : false"
									:disabled="disableNumber === 2 ? loading : false"
									type="danger"
									@button-click="send(1)" />
								<Button
									:class="[
										disableNumber === 1 &&
											loading &&
											'opacity-50 pointer-events-none',
									]"
									:message="
										t('saveMatchBlueWinner', {
											name: getAthleteNameTeam(props.match?.athlete_blue),
										})
									"
									:loading="disableNumber === 2 ? loading : false"
									:disabled="disableNumber === 1 ? loading : false"
									type="primary"
									@button-click="send(2)" />
							</div>
							<div v-if="!isTournament" class="mt-4">
								<Button
									:message="t('saveMatchResult')"
									:loading="loading"
									type="primary"
									@button-click="send(1)" />
							</div>
						</div>
					</div>
				</TransitionChild>
			</div>
		</Dialog>
	</TransitionRoot>
</template>

<script setup>
import CustomInput from "@/components/partials/inputs/customInput.vue";
import RadioGroup from "@/components/partials/inputs/radioGroup.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import Button from "@/components/partials/button.vue";
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import { authApi } from "@/services/api";
import { ref, watch, computed } from "vue";
import { useI18n } from "vue-i18n";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import toast from "@/toast.js";

let { t } = useI18n({ useScope: "global" });

const emit = defineEmits(["close", "sent", "reload", "winner"]);
const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	match: {
		type: Object,
		required: true,
	},
	tournament: {
		type: Object,
		required: true,
	},
	number: {
		type: String,
		required: true,
	},
	savePoints: {
		type: Boolean,
		required: true,
	},
});

let isTournament = computed(() => props.tournament?.category?.category_type?.name === "Tournament");

let endTypes = ref([
	{ value: "normal", name: "endTypes.tournament.normal" },
	{ value: "abdicate", name: "endTypes.tournament.abdicate" },
	{ value: "noShow", name: "endTypes.tournament.noShow" },
	{ value: "disqualified", name: "endTypes.tournament.disqualified" },
	// { value: "double", name: "endTypes.tournament.double" },
]);

let state = ref({
	judge1: {
		name: "",
		round1: {
			athleteRed: "",
			athleteBlue: "",
		},
		round2: {
			athleteRed: "",
			athleteBlue: "",
		},
	},
	judge2: {
		name: "",
		round1: {
			athleteRed: "",
			athleteBlue: "",
		},
		round2: {
			athleteRed: "",
			athleteBlue: "",
		},
	},
	central: {
		name: "",
		round1: {
			athleteRed: "",
			athleteBlue: "",
		},
		round2: {
			athleteRed: "",
			athleteBlue: "",
		},
	},
	endType: "normal",
	number: "",
});
let loading = ref(false);
let saveAsDefault = ref(true);
let open = ref(props.open);
let disableNumber = ref(0);

watch(
	() => props.open,
	(after) => {
		open.value = after;
		let refereesNames = JSON.parse(localStorage.getItem("refereesNames"));
		if (after) {
			if (isTournament.value) {
				endTypes.value = [
					{ value: "normal", name: "endTypes.tournament.normal" },
					{ value: "abdicate", name: "endTypes.tournament.abdicate" },
					{ value: "noShow", name: "endTypes.tournament.noShow" },
					{ value: "disqualified", name: "endTypes.tournament.disqualified" },
					// { value: "double", name: "endTypes.tournament.double" },
				];
			} else {
				endTypes.value = [
					{ value: "normal", name: "endTypes.oneForAll.normal" },
					{ value: "abdicate", name: "endTypes.oneForAll.abdicate" },
					{ value: "noShow", name: "endTypes.oneForAll.noShow" },
					{ value: "disqualified", name: "endTypes.oneForAll.disqualified" },
				];
			}
			state.value = {
				judge1: {
					name: refereesNames?.judge1 || "",
					round1: {
						athleteRed: props.match.points_red_judge1_round1 || "",
						athleteBlue: props.match.points_blue_judge1_round1 || "",
					},
					round2: {
						athleteRed: props.match.points_red_judge1_round2 || "",
						athleteBlue: props.match.points_blue_judge1_round2 || "",
					},
				},
				judge2: {
					name: refereesNames?.judge2 || "",
					round1: {
						athleteRed: props.match.points_red_judge2_round1 || "",
						athleteBlue: props.match.points_blue_judge2_round1 || "",
					},
					round2: {
						athleteRed: props.match.points_red_judge2_round2 || "",
						athleteBlue: props.match.points_blue_judge2_round2 || "",
					},
				},
				central: {
					name: refereesNames?.central_referee || "",
					round1: {
						athleteRed: props.match.points_red_central_referee_round1 || "",
						athleteBlue: props.match.points_blue_central_referee_round1 || "",
					},
					round2: {
						athleteRed: props.match.points_red_central_referee_round2 || "",
						athleteBlue: props.match.points_blue_central_referee_round2 || "",
					},
				},
				endType: "normal",
				number: (Number(props.number) + 1).toString(),
			};
		}
	}
);

function sendPoints() {
	loading.value = true;
	let matchData = getPoints();
	authApi
		.put("matches/noreturn/" + props.match.id, matchData)
		.then(() => {
			loading.value = false;
			emit("reload");
			emit("close");
		})
		.catch(() => {
			loading.value = false;
			toast.error(t("error.pointsNotSaved"));
		});
}

function send(winner) {
	loading.value = true;
	disableNumber.value = winner;

	// Save Judges Names
	let judgesNames = {
		judge1: state.value.judge1.name.trim() || null,
		judge2: state.value.judge2.name.trim() || null,
		central_referee: state.value.central.name.trim() || null,
	};
	if (
		props.tournament.central_referee != judgesNames.central_referee ||
		props.tournament.judge1 != judgesNames.judge1 ||
		props.tournament.judge2 != judgesNames.judge2
	) {
		if (saveAsDefault.value) {
			localStorage.setItem("refereesNames", JSON.stringify(judgesNames));
		}
		authApi.put(`tournaments/${props.tournament.id}/referees`, judgesNames);
	}

	let promises = [];
	let winnerID = null;
	if (props.match.athlete_blue_id == null) {
		winnerID = props.match.athlete_red_id;
	} else winnerID = winner == 1 ? props.match.athlete_red.id : props.match.athlete_blue.id;

	let matchData = getPoints();
	matchData.winner_id = winnerID;
	matchData.normal_win = state.value.endType === "normal";
	matchData.abdicate_win = state.value.endType === "abdicate";
	matchData.no_show_win = state.value.endType === "noShow";
	matchData.disqualified_win = state.value.endType === "disqualified";

	promises.push(authApi.put("matches/noreturn/" + props.match.id, matchData));

	if (
		props.tournament.category.category_type.name == "Tournament" &&
		props.tournament.matches.length > 3
	) {
		if (props.tournament.matches.length == 4) {
			if (props.match.number < 3) promises = getFinalMatches(promises, winner, winnerID);
		}
		if (props.tournament.matches.length == 8) {
			if (props.match.number < 5) promises = getSemiFinalMatches(promises, winner, winnerID);
			else if (props.match.number < 7) promises = getFinalMatches(promises, winner, winnerID);
		}

		if (props.tournament.matches.length == 16) {
			if (props.match.number < 9)
				promises = getQuarterFinalMatches(promises, winner, winnerID);
			else if (props.match.number < 13)
				promises = getSemiFinalMatches(promises, winner, winnerID);
			else if (props.match.number < 15)
				promises = getFinalMatches(promises, winner, winnerID);
		}
		if (props.tournament.matches.length == 32) {
			if (props.match.number < 17) promises = getRound16Matches(promises, winner, winnerID);
			else if (props.match.number < 25)
				promises = getQuarterFinalMatches(promises, winner, winnerID);
			else if (props.match.number < 29)
				promises = getSemiFinalMatches(promises, winner, winnerID);
			else if (props.match.number < 31)
				promises = getFinalMatches(promises, winner, winnerID);
		}
	}

	Promise.all(promises).then(() => {
		authApi
			.post(`tournaments/resolve-podium/${props.tournament.id}`)
			.then(() => {
				emit("sent", state.value.number);
				if (isTournament.value) emit("winner", winner);
				loading.value = false;
				disableNumber.value = 0;
				emit("close");
			})
			.catch((error) => {
				loading.value = false;
				disableNumber.value = 0;
				console.log(error);
				console.log("Error calculation podium");
			});
	});
}

function getRound16Matches(promises, winner, winnerID) {
	let data = {};
	if (props.match.number % 2 === 1) {
		data.athlete_red_id = winnerID;
	} else {
		data.athlete_blue_id = winnerID;
	}
	promises.push(
		authApi.put(
			"matches/noreturn/" +
				props.tournament.matches.find(
					(a) =>
						a.number ==
						props.tournament.matches.length -
							15 +
							Math.floor(((props.match.number - 1) % 32) / 2)
				).id,
			data
		)
	);
	return promises;
}

function getQuarterFinalMatches(promises, winner, winnerID) {
	let data = {};
	if (props.match.number % 2 === 1) {
		data.athlete_red_id = winnerID;
	} else {
		data.athlete_blue_id = winnerID;
	}
	promises.push(
		authApi.put(
			"matches/noreturn/" +
				props.tournament.matches.find(
					(a) =>
						a.number ==
						props.tournament.matches.length -
							7 +
							Math.floor(((props.match.number - 1) % 16) / 2)
				).id,
			data
		)
	);
	return promises;
}

function getSemiFinalMatches(promises, winner, winnerID) {
	let data = {};
	if (props.match.number % 2 === 1) {
		data.athlete_red_id = winnerID;
	} else {
		data.athlete_blue_id = winnerID;
	}
	promises.push(
		authApi.put(
			"matches/noreturn/" +
				props.tournament.matches.find(
					(a) =>
						a.number ==
						props.tournament.matches.length -
							3 +
							Math.floor(((props.match.number - 1) % 8) / 2)
				).id,
			data
		)
	);
	return promises;
}

function getFinalMatches(promises, winner, winnerID) {
	let data = {};
	if (props.match.number % 2 === 1) {
		data.athlete_red_id = winnerID;
	} else {
		data.athlete_blue_id = winnerID;
	}
	promises.push(
		authApi.put(
			"matches/noreturn/" +
				props.tournament.matches.find(
					(a) => a.number == props.tournament.matches.length - 1
				).id,
			data
		)
	);
	data = {};
	if (props.match.number % 2 === 1) {
		data.athlete_red_id =
			winner == 1 ? props.match.athlete_blue.id : props.match.athlete_red.id;
	} else {
		data.athlete_blue_id =
			winner == 1 ? props.match.athlete_blue.id : props.match.athlete_red.id;
	}
	promises.push(
		authApi.put(
			"matches/noreturn/" +
				props.tournament.matches.find((a) => a.number == props.tournament.matches.length)
					.id,
			data
		)
	);
	return promises;
}

function getPoints() {
	let points = {
		points_red_central_referee_round1: getNum(state.value.central.round1.athleteRed),
		points_red_judge1_round1: getNum(state.value.judge1.round1.athleteRed),
		points_red_judge2_round1: getNum(state.value.judge2.round1.athleteRed),
		points_red_central_referee_round2: getNum(state.value.central.round2.athleteRed),
		points_red_judge1_round2: getNum(state.value.judge1.round2.athleteRed),
		points_red_judge2_round2: getNum(state.value.judge2.round2.athleteRed),
		points_red_total: 0,
		points_blue_central_referee_round1: getNum(state.value.central.round1.athleteBlue),
		points_blue_judge1_round1: getNum(state.value.judge1.round1.athleteBlue),
		points_blue_judge2_round1: getNum(state.value.judge2.round1.athleteBlue),
		points_blue_central_referee_round2: getNum(state.value.central.round2.athleteBlue),
		points_blue_judge1_round2: getNum(state.value.judge1.round2.athleteBlue),
		points_blue_judge2_round2: getNum(state.value.judge2.round2.athleteBlue),
		points_blue_total: 0,
	};
	points.points_red_total =
		points.points_red_central_referee_round1 +
		points.points_red_judge1_round1 +
		points.points_red_judge2_round1 +
		points.points_red_central_referee_round2 +
		points.points_red_judge1_round2 +
		points.points_red_judge2_round2;
	points.points_blue_total =
		points.points_blue_central_referee_round1 +
		points.points_blue_judge1_round1 +
		points.points_blue_judge2_round1 +
		points.points_blue_central_referee_round2 +
		points.points_blue_judge1_round2 +
		points.points_blue_judge2_round2;
	return points;
}

function getNum(pointsString) {
	if (pointsString == null) return null;
	if (typeof pointsString !== "string") return pointsString;
	if (pointsString.trim() === "") return null;
	return Number(pointsString.replace(",", ".").trim());
}
</script>
