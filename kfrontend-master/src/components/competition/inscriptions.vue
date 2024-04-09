<template>
	<div>
		<CreateMatchesCompetition
			:open="openCreateMatches"
			:competition-id="props.competitionId"
			@close="openCreateMatches = false" />

		<div class="p-6 text-black text-left mx-auto w-full relative">
			<p class="text-2xl font-semibold text-center">
				{{ t("inscriptionsFor", { name: inscriptionStats?.competition?.name }) }}
			</p>
			<div class="text-lg font-medium text-center">
				<p>
					{{
						t("numberAthletesAccepted", {
							number: inscriptionStats?.athletes?.accepted,
						})
					}}
				</p>
				<p>
					{{
						t("numberAthletesConfirmed", {
							number: inscriptionStats?.athletes?.confirmed,
						})
					}}
				</p>
				<p>
					{{
						t("numberAthletesNotConfirmed", {
							number: inscriptionStats?.athletes?.notConfirmed,
						})
					}}
				</p>
				<div class="h-[0] w-[300px] border-t border-black my-2 mx-auto" />
				<p>
					{{
						t("numberInscriptionsAccepted", {
							number: inscriptionStats?.inscriptions?.accepted,
						})
					}}
				</p>
				<p>
					{{
						t("numberInscriptionsConfirmed", {
							number: inscriptionStats?.inscriptions?.confirmed,
						})
					}}
				</p>
				<p>
					{{
						t("numberInscriptionsNotConfirmed", {
							number: inscriptionStats?.inscriptions?.notConfirmed,
						})
					}}
				</p>
				<router-link
					:to="{
						name: 'Competition Inscriptions Not Confirmed',
						params: { competitionId: props.competitionId },
					}"
					class="text-blue-700 mb-2">
					{{ t("seeInscriptionsNotConfirmed") }}
				</router-link>
				<div class="max-w-max mx-auto">
					<Button
						:size="'small'"
						:message="t('createMatches')"
						type="primary"
						@button-click="openCreateMatches = true" />
				</div>
			</div>
			<div class="max-w-max min-w-max mx-auto">
				<RadioGroup v-if="inscriptions.length != 0" v-model="inscriptionsGroup">
					<div class="mt-4 grid grid-cols-1 gap-y-6 sm:grid-cols-2 sm:gap-x-4 mb-6">
						<RadioGroupOption v-slot="{ checked, active }" as="template" :value="'E'">
							<div
								:class="[
									checked ? 'border-transparent' : 'border-gray-300',
									active ? 'border-indigo-500 ring-2 ring-indigo-500' : '',
									'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
								]">
								<span class="flex flex-1">
									<span class="flex flex-col">
										<RadioGroupLabel
											as="span"
											class="block text-sm font-medium text-gray-900">
											{{ t("groupByTeams") }}
										</RadioGroupLabel>
									</span>
								</span>
								<CheckCircleIcon
									:class="[
										!checked ? 'invisible' : '',
										'h-5 w-5 text-indigo-600 ml-4',
									]"
									aria-hidden="true" />
								<span
									:class="[
										active ? 'border' : 'border-2',
										checked ? 'border-indigo-500' : 'border-transparent',
										'pointer-events-none absolute -inset-px rounded-lg',
									]"
									aria-hidden="true" />
							</div>
						</RadioGroupOption>
						<RadioGroupOption v-slot="{ checked, active }" as="template" :value="'O'">
							<div
								:class="[
									checked ? 'border-transparent' : 'border-gray-300',
									active ? 'border-indigo-500 ring-2 ring-indigo-500' : '',
									'relative flex cursor-pointer rounded-lg border bg-white p-4 shadow-sm focus:outline-none',
								]">
								<span class="flex flex-1">
									<span class="flex flex-col">
										<RadioGroupLabel
											as="span"
											class="block text-sm font-medium text-gray-900">
											{{ t("groupByTournaments") }}
										</RadioGroupLabel>
									</span>
								</span>
								<CheckCircleIcon
									:class="[
										!checked ? 'invisible' : '',
										'h-5 w-5 text-indigo-600 ml-4',
									]"
									aria-hidden="true" />
								<span
									:class="[
										active ? 'border' : 'border-2',
										checked ? 'border-indigo-500' : 'border-transparent',
										'pointer-events-none absolute -inset-px rounded-lg',
									]"
									aria-hidden="true" />
							</div>
						</RadioGroupOption>
					</div>
				</RadioGroup>
			</div>
			<Loading v-if="loading" :size="10" />
			<div v-else>
				<div
					v-if="inscriptionsGroup == 'E'"
					class="inline-flex w-full justify-center space-x-4">
					<div class="w-1/2 justify-end inline-flex">
						<RadioGroup v-model="teamSelected" class="max-w-max">
							<div class="space-y-4">
								<RadioGroupOption
									v-for="inscription in inscriptions"
									:key="inscription.team.id"
									v-slot="{ checked, active }"
									:value="inscription.team.id"
									as="template">
									<div
										:class="[
											checked ? 'border-transparent' : 'border-gray-300',
											active
												? 'border-indigo-500 ring-2 ring-indigo-500'
												: '',
											'relative block cursor-pointer rounded-lg border bg-white px-6 py-4 shadow-sm focus:outline-none sm:flex sm:justify-between',
										]">
										<span class="flex items-center">
											<span class="flex flex-col text-sm">
												<RadioGroupLabel
													as="span"
													class="font-medium text-gray-900 text-xl">
													{{
														`${inscription.team.name} (${inscription.team.abbreviation})`
													}}
												</RadioGroupLabel>
												<RadioGroupDescription
													as="span"
													class="text-gray-500">
													<span class="block sm:inline">
														{{
															`${inscription.team.coach.name} -  ${t(
																"numberInscriptions",
																{
																	number: inscription.inscriptions_length,
																}
															)} -  ${t("numberAthletes", {
																number: inscription.athletes.length,
															})}`
														}}
													</span>
												</RadioGroupDescription>
											</span>
										</span>
										<RadioGroupDescription
											as="span"
											class="mt-2 flex text-sm sm:mt-0 sm:ml-4 sm:flex-col sm:text-right">
											<router-link
												class="ml-10"
												:to="{
													name: 'Inscriptions Team',
													params: {
														competitonId: props.competitionId,
														teamId: inscription.team.id,
													},
												}"
												target="_blank">
												<Button
													:size="'small'"
													:message="t('seeDetails')"
													type="primary"
													@button-click="null" />
											</router-link>
										</RadioGroupDescription>
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
					<div class="w-1/2">
						<div
							v-if="teamSelected != null"
							class="border rounded-lg space-y-4 p-2 w-full sticky top-44">
							<Loading v-if="loadingTeam" :size="10" />
							<div v-else>
								<p class="text-lg font-medium text-right">{{ t("accepted") }}</p>
								<div
									v-for="inscriptionAthlete of inscriptionsTeam"
									:key="inscriptionAthlete.id">
									<p class="font-semibold text-xl">
										{{ getAthleteNameTeam(inscriptionAthlete.athlete) }}
									</p>
									<div
										v-for="inscription of inscriptionAthlete.inscriptions"
										:key="`${inscription.tournament_id}${inscriptionAthlete.athlete_id}`">
										<div class="inline-flex w-full">
											<p>
												{{ getTournamentName(inscription.tournament, t) }}
											</p>
											<a
												v-if="inscription.payment_comprovative_url"
												class="min-w-max link ml-auto"
												target="_blank"
												:href="
													'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
													inscription.payment_comprovative_url
												">
												{{ t("seePaymentComprovative") }}
											</a>
											<p v-else class="min-w-max ml-auto">
												{{ t("noPaymentComprovative") }}
											</p>
											<router-link
												class="mr-2 ml-2 inline-flex text-yellow-500 hover:text-yellow-700 cursor-pointer hover:bg-yellow-100 rounded-full px-4 select-none"
												:to="{
													name: 'Inscription Edit',
													params: {
														tournamentId: inscription.tournament_id,
														athleteCompetitionId:
															inscriptionAthlete.athlete_id,
													},
												}">
												<p class="font-medium">{{ t("edit") }}</p>
												<PencilIcon class="h-5 w-5 mt-0.5 ml-2" />
											</router-link>
											<CheckIcon
												v-if="inscription.accepted"
												class="w-5 h-5 text-green-500 mt-0.5" />
											<XMarkIcon v-else class="w-5 h-5 text-red-500 mt-0.5" />
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div
					v-if="inscriptionsGroup == 'O'"
					class="inline-flex w-full justify-center space-x-4 min-w-xl">
					<div class="w-1/2 justify-end inline-flex">
						<RadioGroup v-model="tournamentSelected" class="max-w-max">
							<div class="space-y-4">
								<RadioGroupOption
									v-for="inscription in inscriptions"
									:key="inscription.tournament.id"
									v-slot="{ checked, active }"
									:value="inscription.tournament.id"
									as="template">
									<div
										:class="[
											checked ? 'border-transparent' : 'border-gray-300',
											active
												? 'border-indigo-500 ring-2 ring-indigo-500'
												: '',
											'relative block cursor-pointer rounded-lg border bg-white px-6 py-4 shadow-sm focus:outline-none sm:flex sm:justify-between',
										]">
										<span class="flex items-center">
											<span class="flex flex-col text-sm min-w-max">
												<RadioGroupLabel
													as="span"
													class="font-medium text-gray-900 text-xl">
													{{
														getTournamentName(inscription.tournament, t)
													}}
												</RadioGroupLabel>
												<RadioGroupDescription
													as="span"
													class="text-gray-500">
													<span class="block sm:inline">
														{{
															t("numberInscriptions", {
																number: inscription.inscriptions_length,
															})
														}}
													</span>
												</RadioGroupDescription>
											</span>
										</span>
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
					<div class="w-1/2">
						<div
							v-if="tournamentSelected != null"
							class="border rounded-lg space-y-1 p-2 w-full sticky lg:top-44 top-4">
							<Loading v-if="loadingTournament" :size="10" />
							<div v-else>
								<div class="inline-flex w-full justify-between">
									<p class="text-lg font-medium">
										{{
											getTournamentName(
												inscriptions.find(
													(a) => a.tournament.id == tournamentSelected
												).tournament,
												t
											)
										}}
									</p>
									<p class="text-lg font-medium">{{ t("accepted") }}</p>
								</div>
								<div
									v-for="inscription of inscriptionsTournament"
									:key="inscription.athlete_competition_id"
									class="inline-flex justify-between w-full">
									<p>
										{{ getAthleteNameTeam(inscription.athlete_competition) }}
									</p>
									<a
										v-if="inscription.payment_comprovative_url"
										class="min-w-max link ml-auto"
										target="_blank"
										:href="
											'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
											inscription.payment_comprovative_url
										">
										{{ t("seePaymentComprovative") }}
									</a>
									<p v-else class="min-w-max ml-auto">
										{{ t("noPaymentComprovative") }}
									</p>
									<router-link
										class="mr-2 ml-2 inline-flex text-yellow-500 hover:text-yellow-700 cursor-pointer hover:bg-yellow-100 rounded-full px-4 select-none"
										:to="{
											name: 'Inscription Edit',
											params: {
												tournamentId: tournamentSelected,
												athleteCompetitionId:
													inscription.athlete_competition_id,
											},
										}">
										<p class="font-medium">{{ t("edit") }}</p>
										<PencilIcon class="h-5 w-5 mt-0.5 ml-2" />
									</router-link>
									<CheckIcon
										v-if="inscription.accepted"
										class="w-5 h-5 text-green-500" />
									<XMarkIcon v-else class="w-5 h-5 text-red-500" />
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import CreateMatchesCompetition from "@/components/competition/modals/createMatchesCompetition.vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import {
	RadioGroup,
	RadioGroupDescription,
	RadioGroupLabel,
	RadioGroupOption,
} from "@headlessui/vue";
import { CheckCircleIcon, XMarkIcon, CheckIcon, PencilIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";
import router from "@/router";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });
const loading = ref(true);
const inscriptions = ref([]);
const inscriptionsTeam = ref([]);
const inscriptionsTournament = ref([]);
const inscriptionsGroup = ref("E");
const teamSelected = ref(null);
const tournamentSelected = ref(null);
const inscriptionStats = ref(null);
const loadingTeam = ref(true);
const loadingTournament = ref(true);
const loadName = ref(true);
const openCreateMatches = ref(false);

const props = defineProps({
	// Competition ID
	competitionId: {
		type: String,
		required: true,
	},
});

watch(
	() => inscriptionsGroup.value,
	() => {
		loadName.value = false;
		getInscriptions();
	}
);

watch(
	() => teamSelected.value,
	(after) => {
		loadingTeam.value = false;
		if (after == null) return;
		loadingTeam.value = true;
		authApi
			.get(
				`inscriptions/competitions/${props.competitionId}/teams/${teamSelected.value}/confirmed/true`
			)
			.then((response) => {
				inscriptionsTeam.value = [];
				for (let inscription of response.data) {
					let index = inscriptionsTeam.value.findIndex(
						(a) => a.athlete.id == inscription.athlete_competition_id
					);
					if (index == -1) {
						index = inscriptionsTeam.value.length;
						inscriptionsTeam.value.push({
							athlete: inscription.athlete_competition,
							athlete_id: inscription.athlete_competition_id,
							inscriptions: [],
						});
					}
					inscriptionsTeam.value[index].inscriptions.push(inscription);
				}
				loadingTeam.value = false;
			})
			.catch((error) => {
				errorHandling(error);
				loadingTeam.value = false;
			});
	}
);

watch(
	() => tournamentSelected.value,
	(after) => {
		loadingTournament.value = false;
		if (after == null) return;
		loadingTournament.value = true;
		authApi
			.get(`inscriptions/tournaments/${tournamentSelected.value}/confirmed/true`)
			.then((response) => {
				inscriptionsTournament.value = response.data;
				console.log(inscriptionsTournament.value);
				loadingTournament.value = false;
			})
			.catch((error) => {
				errorHandling(error);
				loadingTournament.value = false;
			});
	}
);

function getInscriptions() {
	loading.value = true;
	let promises = [];
	if (loadName.value) {
		promises.push(
			authApi
				.get(`inscriptions/competitions/${props.competitionId}/stats`)
				.then(({ data }) => {
					inscriptionStats.value = data;
				})
		);
	}
	let promise =
		inscriptionsGroup.value == "E"
			? authApi.get(`inscriptions/competitions/${props.competitionId}/teams/confirmed/true`)
			: authApi.get(
					`inscriptions/competitions/${props.competitionId}/tournaments/confirmed/true`
			  );
	promises.push(
		promise.then((response) => {
			for (let inscription of response.data) {
				if (inscription.team == null) {
					inscription.team = {
						id: "null",
						name: t("noTeam"),
						abbreviation: "NT",
						coach: {
							name: "",
						},
					};
				}
			}
			inscriptions.value = response.data;
		})
	);
	Promise.all(promises)
		.then(() => {
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
}
getInscriptions();
</script>
