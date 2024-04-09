<template>
	<div class="p-6 text-black text-left mx-auto w-full relative">
		<p class="text-2xl font-semibold text-center">
			{{ t("inscriptionsFor", { name: competitionName }) }}
		</p>
		<p class="mt-2 text-lg font-medium mb-8 text-center">
			{{ t("inscriptionsNotConfirmed", { count: inscriptionsNotConfirmed }) }}
		</p>
		<Loading v-if="loading" :size="10" />
		<div v-else>
			<div class="inline-flex w-full justify-center space-x-4">
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
										active ? 'border-indigo-500 ring-2 ring-indigo-500' : '',
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
											<RadioGroupDescription as="span" class="text-gray-500">
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
				<div class="w-1/2">
					<div
						v-if="teamSelected != null"
						class="border rounded-lg space-y-4 p-2 w-full sticky top-44">
						<Loading v-if="loadingTeam" :size="10" />
						<div v-else>
							<div v-for="inscription of inscriptionsTeam" :key="inscription.id">
								<p class="font-semibold text-xl">
									{{ getAthleteNameTeam(inscription.athlete) }}
								</p>
								<div
									v-for="tournament of inscription.tournaments"
									:key="tournament.id">
									<div class="inline-flex justify-between w-full">
										<p>
											{{ getTournamentName(tournament, t) }}
										</p>
										<router-link
											class="ml-auto mr-10 inline-flex text-yellow-500 hover:text-yellow-700 cursor-pointer hover:bg-yellow-100 rounded-full px-4 select-none"
											:to="{
												name: 'Inscription Edit',
												params: {
													tournamentId: tournament.id,
													athleteCompetitionId: inscription.athlete_id,
												},
											}">
											<p class="font-medium">{{ t("edit") }}</p>
											<PencilIcon class="h-5 w-5 mt-0.5 ml-2" />
										</router-link>
									</div>
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
import Loading from "@/components/partials/loading.vue";
import {
	RadioGroup,
	RadioGroupDescription,
	RadioGroupLabel,
	RadioGroupOption,
} from "@headlessui/vue";
import { PencilIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
let loading = ref(true);
let inscriptions = ref([]);
let inscriptionsTeam = ref([]);
let teamSelected = ref(null);
let competitionName = ref("");
let loadingTeam = ref(true);
let inscriptionsNotConfirmed = ref(0);

const props = defineProps({
	// Competition ID
	competitionId: {
		type: String,
		required: true,
	},
});

let promises = [];
promises.push(
	authApi.get(`competitions/name/${props.competitionId}`).then((response) => {
		competitionName.value = response.data;
	})
);
promises.push(
	authApi
		.get(`inscriptions/competitions/${props.competitionId}/confirmed/false/number`)
		.then((response) => {
			inscriptionsNotConfirmed.value = response.data;
		})
);
promises.push(
	authApi
		.get(`inscriptions/competitions/${props.competitionId}/teams/confirmed/false`)
		.then((response) => {
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

watch(
	() => teamSelected.value,
	() => {
		if (teamSelected.value == null) teamSelected.value = "null";
		loadingTeam.value = true;
		authApi
			.get(
				`inscriptions/competitions/${props.competitionId}/teams/${teamSelected.value}/confirmed/false`
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
							tournaments: [],
						});
					}
					inscriptionsTeam.value[index].tournaments.push(inscription.tournament);
				}
				loadingTeam.value = false;
			})
			.catch((error) => {
				errorHandling(error);
				loadingTeam.value = false;
			});
	}
);
</script>
