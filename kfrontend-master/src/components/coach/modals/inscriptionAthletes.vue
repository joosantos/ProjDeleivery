<template>
	<div>
		<TransitionRoot as="template" :show="open">
			<Dialog as="div" class="fixed z-20 inset-0 overflow-y-auto">
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
					<span
						class="hidden sm:inline-block sm:align-middle sm:h-screen"
						aria-hidden="true">
						&#8203;
					</span>
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
						enter-to="opacity-100 translate-y-0 sm:scale-100"
						leave="ease-in duration-200"
						leave-from="opacity-100 translate-y-0 sm:scale-100"
						leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
						<div
							class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-show shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
							<XCircleIcon
								class="w-10 h-10 text-gray-600 absolute top-4 right-6 hover:text-gray-900 cursor-pointer"
								@click="emit('close')" />
							<Loading v-if="loading" :size="10" />
							<div v-else>
								<div class="w-full justify-between">
									<!-- Modal Tittle -->
									<h3
										class="text-center w-full text-2xl font-medium text-blue-900 mb-6">
										{{ t("signUpAthletes") }}
									</h3>
									<div
										v-if="signUpAthlete && !showConfirm"
										class="-mt-6 ml-auto text-center cursor-pointer text-lg my-1 rounded-md bg-gray-800 inline-flex max-w-max px-4 py-1 text-gray-50 select-none"
										@click="signUpAthlete = false">
										<ArrowLeftIcon class="h-5 w-5 mt-1 mr-1" />
										<p class="ml-1">
											{{ t("return") }}
										</p>
									</div>
									<div
										v-if="showConfirm"
										class="-mt-6 ml-auto text-center cursor-pointer text-lg my-1 rounded-md bg-gray-800 inline-flex max-w-max px-4 py-1 text-gray-50 select-none"
										@click="showConfirm = false">
										<ArrowLeftIcon class="h-5 w-5 mt-1 mr-1" />
										<p class="ml-1">
											{{ t("return") }}
										</p>
									</div>
									<RadioGroup
										v-if="!signUpAthlete && !signUpTeam && !showConfirm"
										v-model="teamSignUp">
										<div
											class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4 mb-6">
											<RadioGroupOption
												v-for="signUpType in signUpTypeList"
												:key="signUpType.value"
												v-slot="{ checked, active }"
												as="template"
												:value="signUpType.value">
												<div
													:class="[
														checked
															? 'border-transparent'
															: 'border-gray-300',
														active
															? 'border-indigo-500 ring-2 ring-indigo-500'
															: '',
														'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
													]">
													<span class="flex flex-1">
														<span class="flex flex-col">
															<RadioGroupLabel
																as="span"
																class="block text-sm font-medium text-gray-900">
																{{ t(signUpType.label) }}
															</RadioGroupLabel>
														</span>
													</span>
													<CheckCircleIcon
														:class="[
															!checked ? 'invisible' : '',
															'h-5 w-5 text-indigo-600',
														]"
														aria-hidden="true" />
													<span
														:class="[
															active ? 'border' : 'border-2',
															checked
																? 'border-indigo-500'
																: 'border-transparent',
															'pointer-events-none absolute -inset-px rounded-lg',
														]"
														aria-hidden="true" />
												</div>
											</RadioGroupOption>
										</div>
									</RadioGroup>
								</div>
								<div v-if="showConfirm">
									<RadioGroup
										v-if="inscriptionsAthlete.length != 0"
										v-model="showAthleteInscriptions">
										<div
											class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4 mb-6">
											<RadioGroupOption
												v-slot="{ checked, active }"
												as="template"
												:value="true">
												<div
													:class="[
														checked
															? 'border-transparent'
															: 'border-gray-300',
														active
															? 'border-indigo-500 ring-2 ring-indigo-500'
															: '',
														'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
													]">
													<span class="flex flex-1">
														<span class="flex flex-col">
															<RadioGroupLabel
																as="span"
																class="block text-sm font-medium text-gray-900">
																{{ t("inscriptionsShow.athletes") }}
															</RadioGroupLabel>
														</span>
													</span>
													<CheckCircleIcon
														:class="[
															!checked ? 'invisible' : '',
															'h-5 w-5 text-indigo-600',
														]"
														aria-hidden="true" />
													<span
														:class="[
															active ? 'border' : 'border-2',
															checked
																? 'border-indigo-500'
																: 'border-transparent',
															'pointer-events-none absolute -inset-px rounded-lg',
														]"
														aria-hidden="true" />
												</div>
											</RadioGroupOption>
											<RadioGroupOption
												v-slot="{ checked, active }"
												as="template"
												:value="false">
												<div
													:class="[
														checked
															? 'border-transparent'
															: 'border-gray-300',
														active
															? 'border-indigo-500 ring-2 ring-indigo-500'
															: '',
														'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
													]">
													<span class="flex flex-1">
														<span class="flex flex-col">
															<RadioGroupLabel
																as="span"
																class="block text-sm font-medium text-gray-900">
																{{
																	t(
																		"inscriptionsShow.tournaments"
																	)
																}}
															</RadioGroupLabel>
														</span>
													</span>
													<CheckCircleIcon
														:class="[
															!checked ? 'invisible' : '',
															'h-5 w-5 text-indigo-600',
														]"
														aria-hidden="true" />
													<span
														:class="[
															active ? 'border' : 'border-2',
															checked
																? 'border-indigo-500'
																: 'border-transparent',
															'pointer-events-none absolute -inset-px rounded-lg',
														]"
														aria-hidden="true" />
												</div>
											</RadioGroupOption>
										</div>
									</RadioGroup>
									<div
										v-if="inscriptionsAthlete.length == 0"
										class="font-semibold text-center text-xl">
										<p>{{ t("noneToConfirm") }}</p>
									</div>
									<div v-if="showAthleteInscriptions" class="space-y-4">
										<div
											v-for="athlete of inscriptionsAthlete"
											:key="athlete.id">
											<p class="font-semibold text-lg">
												{{
													`${athlete.name} - - - ${
														athlete.tournaments.length
													} ${t("tournaments")}`
												}}
											</p>
											<div
												v-for="tournament of athlete.tournaments"
												:key="tournament.id">
												<p>
													{{ `${getTournamentName(tournament, t)}` }}
												</p>
											</div>
										</div>
									</div>
									<div v-else class="space-y-4">
										<div
											v-for="tournament of inscriptionsTournament"
											:key="tournament.id">
											<p class="font-semibold text-lg">
												{{
													`${tournament.name} - - - ${
														tournament.athletes.length
													} ${t("athletes")}`
												}}
											</p>
											<div
												v-for="athlete of tournament.athletes"
												:key="athlete.id">
												<p>
													{{ `${getAthleteNameTeam(athlete)}` }}
												</p>
											</div>
										</div>
									</div>
									<div class="mt-4">
										<Button
											:loading="showSpinningWheel"
											:show-x="showXConfirm"
											:message="t('confirm')"
											type="primary"
											@button-click="confirmInscriptions" />
									</div>
								</div>
								<div v-else>
									<!-- Choose atlhetes to the team -->
									<div v-if="teamSignUp && !signUpAthlete">
										<div class="grid gap-x-4 grid-cols-2 w-full">
											<div>
												<div v-for="athlete of athletes" :key="athlete.id">
													<div
														v-show="
															athlete.inTeam == null ||
															!athlete.inTeam
														"
														class="w-full border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-200 hover:border-gray-400 px-2 mt-2"
														@click="athlete.inTeam = true">
														{{ athlete.name }}
													</div>
												</div>
											</div>
											<div>
												<div v-for="athlete of athletes" :key="athlete.id">
													<div
														v-show="
															athlete.inTeam != null && athlete.inTeam
														"
														class="w-full border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-200 hover:border-gray-400 px-2 mt-2"
														@click="athlete.inTeam = false">
														{{ athlete.name }}
													</div>
												</div>
											</div>
										</div>
										<div class="relative mt-14">
											<Button
												:message="t('signUpTeamButton')"
												type="primary"
												@button-click="startSingingTeam" />
										</div>
									</div>
									<!-- Choose tournaments to signUp an athlete or a team -->
									<div v-else-if="signUpAthlete" class="w-full relative">
										<fieldset>
											<legend class="text-lg font-medium text-gray-900">
												{{ t("signUp", { name: athleteToSign.name }) }}
											</legend>
											<div
												class="mt-4 divide-y divide-gray-200 border-t border-b border-gray-200">
												<div
													v-for="(
														tournament, tournamentIdx
													) in tournamentsAvailable"
													:key="tournamentIdx"
													class="relative flex items-start py-4"
													@click="tournament.signUp = !tournament.signUp">
													<div class="min-w-0 flex-1 text-sm">
														<p
															class="select-none font-medium text-gray-700">
															{{ getTournamentName(tournament, t) }}
														</p>
													</div>
													<div class="ml-3 flex h-5 items-center">
														<input
															:id="`person-${tournament.id}`"
															v-model="tournament.signUp"
															:name="`person-${tournament.id}`"
															type="checkbox"
															class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
													</div>
												</div>
												<div class="mt-16">
													<Button
														:loading="showSpinningWheel"
														:show-x="showX"
														:message="t('signUpButton')"
														type="primary"
														@button-click="signUp" />
												</div>
											</div>
										</fieldset>
									</div>
									<!-- Choose atlhete to Sign Up -->
									<div v-else class="space-y-2">
										<div v-for="athlete of athletes" :key="athlete.id">
											<div
												class="w-full border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-200 hover:border-gray-400 px-2"
												@click="startSinging(athlete)">
												{{ athlete.name }}
											</div>
										</div>
									</div>
									<div v-if="!signUpAthlete" class="mt-4">
										<Button
											:message="t('confirm')"
											type="primary"
											@button-click="showConfirm = true" />
									</div>
								</div>
							</div>
						</div>
					</TransitionChild>
				</div>
			</Dialog>
		</TransitionRoot>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import {
	Dialog,
	DialogOverlay,
	TransitionChild,
	TransitionRoot,
	RadioGroup,
	RadioGroupLabel,
	RadioGroupOption,
} from "@headlessui/vue";
import { ArrowLeftIcon, CheckCircleIcon } from "@heroicons/vue/24/solid";
import { XCircleIcon } from "@heroicons/vue/24/outline";
import { onMounted, ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam, getAge } from "@/services/athlete.service.js";

let { t } = useI18n();

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	competitionId: {
		type: String,
		required: true,
	},
	teamId: {
		type: String,
		required: true,
	},
	competitionStart: {
		type: String,
		required: true,
	},
	competitionCalculateAgeStartYear: {
		type: Boolean,
		required: true,
	},
});

const emit = defineEmits(["close", "created", "updated"]);

let loading = ref(true);
let open = ref(props.open);
let showSpinningWheel = ref(false);
let showX = ref(false);
let showXConfirm = ref(false);
let signUpAthlete = ref(false);
let athleteToSign = ref(null);
let competition = ref(null);
let tournamentsAvailable = ref([]);
let athleteCompetition = ref(null);
let teamSignUp = ref(false);
let signUpTypeList = ref([
	{ value: false, label: "signUpType.individual" },
	{ value: true, label: "signUpType.team" },
]);
let signUpTeam = ref(false);
let athletesTeam = ref([]);
let showConfirm = ref(false);
let inscriptions = ref([]);
let inscriptionsTournament = ref([]);
let inscriptionsAthlete = ref([]);
let showAthleteInscriptions = ref(true);
const athletes = ref([]);

onMounted(async () => {
	try {
		const { data } = await authApi.get(
			`athletes?teams=${[props.teamId]}&limit=-1&federated=true`
		);
		athletes.value = data.results;
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
});

watch(
	() => props.open,
	async (after) => {
		open.value = after;
		if (after) {
			loading.value = !athletes.value.length;
			showSpinningWheel.value = false;
			showX.value = false;
			showXConfirm.value = false;
			signUpAthlete.value = false;
			athleteToSign.value = null;
			competition.value = null;
			tournamentsAvailable.value = [];
			athleteCompetition.value = null;
			teamSignUp.value = false;
			signUpTeam.value = false;
			athletesTeam.value = [];
			showConfirm.value = false;
			inscriptions.value = [];
			inscriptionsTournament.value = [];
			inscriptionsAthlete.value = [];
			showAthleteInscriptions.value = false;
		}
	}
);

watch(
	() => showConfirm.value,
	(after) => {
		if (after) {
			getInscriptions();
		}
	}
);

function startSinging(athlete) {
	loading.value = true;
	athleteToSign.value = athlete;
	athleteToSign.value.age = getAge(
		athleteToSign.value.birthday,
		props.competitionCalculateAgeStartYear,
		props.competitionStart
	);
	tournamentsAvailable.value = [];
	athleteCompetition.value = null;
	authApi
		.get(`competitions/inscriptions/${props.competitionId}`)
		.then((response) => {
			competition.value = response.data;
			for (let tournament of competition.value.tournaments) {
				if (tournament.category.team_category) continue;
				if (
					tournament.category.name.toLowerCase().indexOf("adaptado") == -1 &&
					tournament.category.name.toLowerCase().indexOf("adapted") == -1
						? athleteToSign.value.is_adapted
						: !athleteToSign.value.is_adapted
				)
					continue;

				if (
					tournament.is_male == null ||
					tournament.is_male == athleteToSign.value.is_male
				) {
					if (
						(tournament.age_min == null && tournament.age_max == null) ||
						(tournament.age_min == null
							? true
							: tournament.age_min <= athleteToSign.value.age &&
							  (tournament.age_max == null
									? true
									: tournament.age_max >= athleteToSign.value.age))
					) {
						if (
							(tournament.weight_min == null && tournament.weight_max == null) ||
							((tournament.weight_min == null
								? true
								: tournament.weight_min + 0.6 <= athleteToSign.value.weight) &&
								(tournament.weight_max == null
									? true
									: tournament.weight_max + 0.5 >= athleteToSign.value.weight))
						) {
							if (
								tournament.belt_min_id == null ||
								(tournament.belt_min.order <= athleteToSign.value.belt.order &&
									tournament.belt_max.order >= athleteToSign.value.belt.order)
							) {
								tournament.alreadySignedUp = false;
								tournament.signUp = false;
								inscriptionLoop: for (let inscription of tournament.inscriptions) {
									if (inscription.athlete_competition.athletes_group.length != 1)
										continue;
									for (let athlete_group of inscription.athlete_competition
										.athletes_group) {
										if (athlete_group.athlete.id == athleteToSign.value.id) {
											tournament.alreadySignedUp = true;
											tournament.signUp = true;
											athleteCompetition.value =
												inscription.athlete_competition;
											break inscriptionLoop;
										}
									}
								}
								if (
									tournament.weight_min != null ||
									tournament.weight_max != null
								) {
									let index = 0;
									let newWeight =
										tournament.weight_min == null
											? tournament.weight_max
											: tournament.weight_min;
									let oldWeight = 0;
									let notFound = true;
									for (let tourn of tournamentsAvailable.value) {
										if (tourn.category.name == tournament.category.name) {
											notFound = false;

											oldWeight =
												tourn.weight_min == null
													? tourn.weight_max
													: tourn.weight_min;
											if (newWeight < oldWeight) {
												tournamentsAvailable.value.splice(index, 1);
												tournamentsAvailable.value.push(tournament);
												break;
											}
										}
										index += 1;
									}
									if (notFound) tournamentsAvailable.value.push(tournament);
								} else tournamentsAvailable.value.push(tournament);
							}
						}
					}
				}
			}
			signUpAthlete.value = true;
			loading.value = false;
		})
		.catch((e) => {
			console.error(e);
			loading.value = false;
		});
}

function startSingingTeam() {
	loading.value = true;
	let name = "";
	athletesTeam.value = [];
	for (let athlete of athletes.value) {
		if (athlete.inTeam != null && athlete.inTeam) {
			athletesTeam.value.push(athlete);
			name += athlete.name + ",";
		}
	}
	let aux = name.split(",");
	name = aux.slice(0, aux.length - 2).join(" ") + ", " + t("and") + " " + aux[aux.length - 2];

	if (athletesTeam.value.length <= 1) {
		toast.error(t("error.athletesTeamSize"));
		loading.value = false;
		return;
	}

	athleteToSign.value = { name: name };
	athleteCompetition.value = null;

	tournamentsAvailable.value = [];
	authApi
		.get(`competitions/inscriptions/${props.competitionId}`)
		.then((response) => {
			competition.value = response.data;
			for (let tournament of competition.value.tournaments) {
				let canSignUpTournament = false;
				if (
					!tournament.category.team_category ||
					tournament.category.team_number != athletesTeam.value.length
				)
					continue;
				let maxAge = 0;
				let maxBeltOrder = 0;
				let maxWeight = 0;
				let isOpen = false;
				let isMasc = athletesTeam.value[0].is_male;
				for (let athlete of athletesTeam.value) {
					athlete.age = getAge(
						athlete.birthday,
						props.competitionCalculateAgeStartYear,
						props.competitionStart
					);
					if (athlete.age > maxAge) maxAge = athlete.age;
					if (athlete.weight > maxWeight) maxWeight = athlete.weight;
					if (athlete.belt.order > maxBeltOrder) maxBeltOrder = athlete.belt.order;
					if (athlete.is_male != isMasc) isOpen = true;
				}

				if (tournament.is_male == null || (tournament.is_male == isMasc && !isOpen)) {
					if (
						(tournament.age_min == null && tournament.age_max == null) ||
						(tournament.age_min == null
							? true
							: tournament.age_min <= maxAge &&
							  (tournament.age_max == null ? true : tournament.age_max >= maxAge))
					) {
						if (
							(tournament.weight_min == null && tournament.weight_max == null) ||
							((tournament.weight_min == null
								? true
								: tournament.weight_min + 0.6 <= maxWeight) &&
								(tournament.weight_max + 0.5 == null
									? true
									: tournament.weight_max >= maxWeight))
						) {
							if (
								tournament.belt_min_id == null ||
								(tournament.belt_min.order <= maxBeltOrder &&
									tournament.belt_max.order >= maxBeltOrder)
							)
								canSignUpTournament = true;
						}
					}
				}

				if (canSignUpTournament) {
					tournament.alreadySignedUp = false;
					tournament.signUp = false;
					for (let inscription of tournament.inscriptions) {
						let alreadySignedUp = true;
						groupLoop: for (let athlete_group of inscription.athlete_competition
							.athletes_group) {
							for (let athlete of athletesTeam.value) {
								if (athlete_group.athlete.id == athlete.id) {
									continue groupLoop;
								}
							}
							alreadySignedUp = false;
						}
						if (alreadySignedUp) {
							tournament.alreadySignedUp = true;
							tournament.signUp = true;
							athleteCompetition.value = inscription.athlete_competition;
							break;
						}
					}
					if (tournament.weight_min != null || tournament.weight_max != null) {
						let index = 0;
						let newWeight =
							tournament.weight_min == null
								? tournament.weight_max
								: tournament.weight_min;
						let oldWeight = 0;
						let notFound = true;
						for (let tourn of tournamentsAvailable.value) {
							if (tourn.category.name == tournament.category.name) {
								notFound = false;

								oldWeight =
									tourn.weight_min == null ? tourn.weight_max : tourn.weight_min;
								if (newWeight < oldWeight && maxWeight < newWeight) {
									tournamentsAvailable.value.splice(index, 1);
									tournamentsAvailable.value.push(tournament);
									break;
								}
							}
							index += 1;
						}
						if (notFound) tournamentsAvailable.value.push(tournament);
					} else tournamentsAvailable.value.push(tournament);
				}
			}
			signUpAthlete.value = true;
			loading.value = false;
		})
		.catch((error) => {
			console.log(error);
			loading.value = false;
		});
}

function signUp() {
	loading.value = true;
	showSpinningWheel.value = true;
	showX.value = false;
	if (teamSignUp.value) {
		signUpAthletesTeam();
		loading.value = false;
		return;
	}
	if (athleteCompetition.value == null) {
		authApi
			.post(`competitions/${competition.value.id}/athlete-competition`, {
				competition_id: competition.value.id,
			})
			.then((response) => {
				athleteCompetition.value = response.data;
				authApi
					.post(`athletes-group`, {
						athlete_id: athleteToSign.value.id,
						athlete_competition_id: athleteCompetition.value.id,
					})
					.then(() => {
						createInscriptions(athleteCompetition.value);
					});
			})
			.catch((error) => {
				errorHandling(error);
				showSpinningWheel.value = false;
				showX.value = true;
				loading.value = false;
			});
	} else {
		createInscriptions(athleteCompetition.value);
	}
}

function signUpAthletesTeam() {
	loading.value = true;
	if (athleteCompetition.value == null) {
		authApi
			.post(`competitions/${competition.value.id}/athlete-competition`, {
				competition_id: competition.value.id,
			})
			.then((response) => {
				athleteCompetition.value = response.data;
				let promise = [];
				for (let athlete of athletesTeam.value) {
					authApi.post(`athletes-group`, {
						athlete_id: athlete.id,
						athlete_competition_id: athleteCompetition.value.id,
					});
				}
				Promise.all(promise).then(() => {
					createInscriptions(athleteCompetition.value);
				});
			})
			.catch((error) => {
				loading.value = false;
				errorHandling(error);
				showSpinningWheel.value = false;
				showX.value = true;
			});
	} else {
		createInscriptions(athleteCompetition.value);
	}
}

function createInscriptions(athleteCompetition) {
	loading.value = true;
	let promises = [];
	let deleted = 0;
	let signed = 0;
	let newSigns = 0;
	for (let tournament of tournamentsAvailable.value) {
		if (tournament.alreadySignedUp) signed += 1;
		if (tournament.alreadySignedUp && !tournament.signUp) {
			deleted += 1;
			promises.push(
				authApi.delete(`inscriptions/tournaments/${tournament.id}/${athleteCompetition.id}`)
			);
			continue;
		}
		if (tournament.alreadySignedUp) continue;
		if (!tournament.signUp) continue;
		newSigns += 1;

		promises.push(
			authApi.post(`inscriptions/tournaments/${tournament.id}/${athleteCompetition.id}`)
		);
	}

	Promise.all(promises)
		.then(() => {
			if (signed == deleted && newSigns == 0 && signed != 0) {
				let groupPromises = [];
				for (let athlete_group of athleteCompetition.athletes_group) {
					groupPromises.push(
						authApi.delete(
							`athletes-group/${athlete_group.athlete_competition_id}/${athlete_group.athlete_id}`
						)
					);
				}
				Promise.all(groupPromises).then(() => {
					authApi
						.delete(
							`competitions/${competition.value.id}/athlete-competition/${athleteCompetition.id}`
						)
						.then(() => {
							showSpinningWheel.value = false;
							toast.success(t("singedUp"));
							signUpAthlete.value = false;
							loading.value = false;
						});
				});
			} else {
				showSpinningWheel.value = false;
				toast.success(t("singedUp"));
				signUpAthlete.value = false;
				loading.value = false;
			}
		})
		.catch((error) => {
			showSpinningWheel.value = false;
			showX.value = true;
			errorHandling(error);
			loading.value = false;
		});
}

function getInscriptions() {
	loading.value = true;
	authApi
		.get(
			`inscriptions/competitions/${props.competitionId}/teams/${props.teamId}/confirmed/false`
		)
		.then((response) => {
			inscriptions.value = response.data;
			groupInscriptions();
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
}

function groupInscriptions() {
	inscriptionsTournament.value = [];
	inscriptionsAthlete.value = [];
	for (let inscription of inscriptions.value) {
		let tournName = getTournamentName(inscription.tournament, t);
		let index = inscriptionsTournament.value.findIndex((a) => {
			return a.name == tournName;
		});

		if (index == -1) {
			index = inscriptionsTournament.value.length;
			inscriptionsTournament.value.push({
				name: tournName,
				athletes: [],
				id: inscription.tournament.id,
			});
		}
		inscriptionsTournament.value[index].athletes.push(inscription.athlete_competition);

		let atName = getAthleteNameTeam(inscription.athlete_competition);
		index = inscriptionsAthlete.value.findIndex((a) => {
			return a.name == atName;
		});

		if (index == -1) {
			index = inscriptionsAthlete.value.length;
			inscriptionsAthlete.value.push({
				name: atName,
				tournaments: [],
				id: inscription.athlete_competition_id,
			});
		}
		inscriptionsAthlete.value[index].tournaments.push(inscription.tournament);
	}
	inscriptionsTournament.value.sort((a, b) => {
		if (a.name < b.name) {
			return -1;
		}
		if (a.name > b.name) {
			return 1;
		}
		return 0;
	});
}

function confirmInscriptions() {
	showSpinningWheel.value = true;
	let updateList = [];
	for (let inscription of inscriptions.value) {
		updateList.push({
			athlete_competition_id: inscription.athlete_competition_id,
			tournament_id: inscription.tournament_id,
			confirmed: true,
		});
	}
	authApi
		.put("inscriptions/confirm/list", updateList)
		.then(() => {
			toast.success(t("confirmed"));
			showConfirm.value = false;
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
}
</script>

<i18n>
{
	"en_GB": {
		"noneToConfirm": "No inscriptions to confirm",
		"confirmed": "Inscriptions Confirmed",
		"tournaments": "Tournaments",
		"athletes": "Athletes",
		"inscriptionsShow": {
			"athletes": "Show Inscriptions by Athlete",
			"tournaments": "Show Inscriptions by Tournament",
		},
		"confirm": "Confirm Inscriptions",
		"return": "Return to athletes list",
		"signUpAthletes": "Sign Up Athletes",
		"fed": "Fed. nº ",
		"signUp": "Sign Up {name}",
		"signUpButton": "Sign Up Athlete",
		"singedUp": "Athlete Signed Up",
		"signUpTeams": "Sign Up to teams tournaments",
		"signUpType": {
			"individual": "Individual",
			"team": "Teams"
		},
		"signUpTeamButton": "Sign Up Team",
		"error": {
			"athletesTeamSize": "The team need at least 2 members"
		},
		"and": "and",
        "open": "Open",
        "masc": "Masc.",
        "fem": "Fem.",
		"year": "{count} Year | {count} Years",
		"belts": {
			"white": "White",
			"white-yellow": "White and Yellow",
			"yellow": "Yellow",
			"yellow-orange": "Yellow and Orange",
			"orange": "Orange",
			"orange-purple": "Orange and Purple",
			"purple": "Purple",
			"purple-blue": "Purple and Blue",
			"blue": "Blue",
			"blue-green": "Blue and Green",
			"green": "Green",
			"brown-jr": "Brown Junior",
			"brown": "Brown",
			"black-jr": "Black Junior",
			"black": "Black",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
	"pt_PT": {
		"noneToConfirm": "Sem inscrições para confirmar",
		"confirmed": "Inscrições Confirmadas",
		"tournaments": "Torneios",
		"athletes": "Atletas",
		"inscriptionsShow": {
			"athletes": "Mostrar Inscrições por Atleta",
			"tournaments": "Mostrar Inscrições por Torneio",
		},
		"confirm": "Confirmar Inscrições",
		"return": "Voltar à lista de atletas",
		"signUpAthletes": "Inscrever Atletas",
		"fed": "Fed. nº ",
		"signUp": "Inscrever {name}",
		"signUpButton": "Inscrever Atleta",
		"singedUp": "Atleta Inscrito",
		"signUpTeams": "Inscrever em torneios de equipa",
		"signUpType": {
			"individual": "Individual",
			"team": "Equipas"
		},
		"signUpTeamButton": "Inscrever Equipa",
		"error": {
			"athletesTeamSize": "A equipa necessita de pelo menos 2 membros"
		},
		"and": "e",
		"open": "Aberto",
		"masc": "Masculino",
		"fem": "Feminino",
		"year": "{count} Ano | {count} Anos",
		"belts": {
			"white": "Branco",
			"white-yellow": "Branco e Amarelo",
			"yellow": "Amarelo",
			"yellow-orange": "Amarelo e Laranja",
			"orange": "Laranja",
			"orange-purple": "Laranja e Púrpura",
			"purple": "Púrpura",
			"purple-blue": "Púrpura e Azul",
			"blue": "Azul",
			"blue-green": "Azul e Verde",
			"green": "Verde",
			"brown-jr": "Castanho Junior",
			"brown": "Castanho",
			"black-jr": "Preto Junior",
			"black": "Preto",
			"duan-1": "Duan 1",
			"duan-2": "Duan 2",
			"duan-3": "Duan 3+",
		},
	},
}
</i18n>
