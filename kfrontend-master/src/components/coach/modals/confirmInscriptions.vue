<template>
	<div>
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
							<Loading v-if="loading" :size="10" />
							<div v-else class="p-6 max-w-max text-black text-left mx-auto">
								<div class="max-w-max mx-auto mb-12">
									<RadioGroup
										:label="t('inscriptionsGroup')"
										:name="'inscriptionsGroup'"
										:option-selected="inscriptionsGroup"
										:radio-options="[
											{ name: t('team'), value: 'E' },
											{ name: t('tourn'), value: 'O' },
										]"
										:error="''"
										@selected="(option) => (inscriptionsGroup = option)" />
								</div>
								<div v-if="inscriptionsGroup == 'E'" class="space-y-4">
									<div v-for="team of inscriptionsTeam" :key="team.id">
										<p class="font-semibold text-lg">
											{{
												`${team.coach} - ${team.name} (${
													team.abbreviation
												}) - - - ${team.inscriptions.length} ${t(
													"athletes"
												)}`
											}}
										</p>
										<div
											v-for="inscription of team.inscriptions"
											:key="inscription.id">
											<p>
												{{
													`${inscription.name} (${inscription.tournaments.length})`
												}}
											</p>
										</div>
									</div>
								</div>
								<div v-if="inscriptionsGroup == 'O'" class="space-y-4">
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
import RadioGroup from "@/components/partials/inputs/radioGroup.vue";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();
let loading = ref(true);
let inscriptions = ref([]);
let inscriptionsTeam = ref([]);
let inscriptionsTournament = ref([]);
let inscriptionsGroup = ref("E");

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	// Team ID
	teamId: {
		type: String,
		required: true,
	},
});

let open = ref(props.open);
watch(
	() => props.open,
	(after) => {
		open.value = after;
	}
);

function getInscriptions() {
	loading.value = true;
	authApi
		.get(`inscriptions/competitions/${props.competitionId}`)
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
getInscriptions();

function groupInscriptions() {
	for (let inscription of inscriptions.value) {
		let team = inscription.athlete_competition.athletes_group[0].athlete.team;
		let index = inscriptionsTeam.value.findIndex((a) => {
			return a.name == team.name;
		});
		if (index == -1) {
			index = inscriptionsTeam.value.length;
			inscriptionsTeam.value.push({
				name: team.name,
				coach: team.coach.name,
				id: team.id,
				abbreviation: team.abbreviation,
				inscriptions: [],
			});
		}
		let athleteName = getAthleteNameTeam(inscription.athlete_competition).split("(")[0].trim();
		let teamIndex = inscriptionsTeam.value[index].inscriptions.findIndex((a) => {
			return a.name == athleteName;
		});
		if (teamIndex == -1) {
			teamIndex = inscriptionsTeam.value[index].inscriptions.length;
			inscriptionsTeam.value[index].inscriptions.push({
				name: athleteName,
				tournaments: [],
			});
		}
		inscriptionsTeam.value[index].inscriptions[teamIndex].tournaments.push(
			inscription.tournament
		);
		let tournName = getTournamentName(inscription.tournament, t);
		index = inscriptionsTournament.value.findIndex((a) => {
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
	}
	inscriptionsTeam.value.sort((a, b) => {
		if (a.name < b.name) {
			return -1;
		}
		if (a.name > b.name) {
			return 1;
		}
		return 0;
	});
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
</script>

<i18n>
{
  	"en_GB": {
        "athletes": "Athletes",
        "tournaments": "Tournaments",
        "inscriptionsGroup": "Group Inscriptions By:",
        "team": "Teams",
        "tourn": "Tournaments",
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
        "athletes": "Atletas",
        "tournaments": "Torneios",
        "inscriptionsGroup": "Agrupar Inscrições por:",
        "team": "Equipas",
        "tourn": "Torneios",
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
	}
}
</i18n>
