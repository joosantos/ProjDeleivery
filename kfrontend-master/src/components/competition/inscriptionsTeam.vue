<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="p-6 max-w-max text-black text-left mx-auto">
		<p class="text-2xl font-semibold text-center">
			{{ competitionName }}
		</p>
		<p class="text-2xl font-semibold text-center">
			{{
				`${
					inscriptions?.at(0)?.athlete_competition?.athletes_group?.at(0)?.athlete?.team
						?.name || t("noTeam")
				} (${
					inscriptions?.at(0)?.athlete_competition?.athletes_group?.at(0)?.athlete?.team
						?.abbreviation || "NT"
				})`
			}}
		</p>
		<div class="space-y-4 mt-8">
			<ul role="list" class="relative z-0 divide-y divide-gray-200">
				<li class="w-full">
					<div
						class="inline-flex max-w-max relative left-1/2 -translate-x-1/2 cursor-pointer">
						<div
							:class="[
								'w-60 border rounded-l-lg px-2 py-4',
								orderByTournament
									? 'border-blue-700 bg-blue-100'
									: 'border-gray-400 bg-gray-50 border-r-0',
							]"
							@click="orderByTournament = true">
							<p class="text-center">{{ t("showByTournaments") }}</p>
						</div>
						<div
							:class="[
								'w-60 border rounded-r-lg px-2 py-4',
								orderByTournament
									? 'border-gray-400 bg-gray-50 border-l-0'
									: 'border-blue-700 bg-blue-100',
							]"
							@click="orderByTournament = false">
							<p class="text-center">{{ t("showByAthletes") }}</p>
						</div>
					</div>
					<div class="w-full inline-flex justify-between mt-4">
						<div>
							<label for="acceptAll" class="text-lg font-medium">{{
								t(acceptAll ? "refuseAllAthletes" : "acceptAllAthletes")
							}}</label>
							<input
								v-model="acceptAll"
								name="acceptAll"
								type="checkbox"
								class="ml-2 mb-0.5" />
						</div>
						<div>
							<Button
								:loading="showSpinningWheel"
								:message="t('copyListOfInscriptionsAccepted')"
								type="primary"
								size="small"
								@button-click="copyList" />
						</div>
					</div>
				</li>
				<li
					v-if="orderByTournament"
					v-for="tournament of inscriptionsTournament"
					:key="tournament.tournament_id"
					class="bg-white">
					<div class="relative flex items-center space-x-3 px-6 py-5">
						<div class="min-w-0 flex-1">
							<div>
								<!-- Extend touch target to entire panel -->
								<p class="text-xl font-semibold text-gray-900">
									{{ tournament.name }}
								</p>
								<div
									v-for="athlete of tournament.athletes"
									:key="athlete.athlete_id">
									<div
										class="inline-flex ml-4 w-full"
										@click="
											() =>
												toogleInscription(
													tournament.tournament_id,
													athlete.athlete_id
												)
										">
										<p>
											{{ `${getAthleteNameTeam(athlete.athlete)}` }}
										</p>
										<a
											v-if="athlete.payment_comprovative_url"
											class="min-w-max link ml-auto"
											target="_blank"
											:href="
												'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
												athlete.payment_comprovative_url
											">
											{{ t("seePaymentComprovative") }}
										</a>
										<p v-else class="min-w-max ml-auto">
											{{ t("noPaymentComprovative") }}
										</p>
										<input
											v-model="athlete.accepted"
											value="true"
											type="checkbox"
											class="mt-1 ml-2 rounded-sm" />
									</div>
								</div>
							</div>
						</div>
					</div>
				</li>
				<li
					v-else
					v-for="athlete of inscriptionsAthletes"
					:key="athlete.athlete_id"
					class="bg-white">
					<div class="relative flex items-center space-x-3 px-6 py-5">
						<div class="min-w-0 flex-1">
							<div>
								<!-- Extend touch target to entire panel -->
								<p class="text-xl font-semibold text-gray-900">
									{{ athlete.name }}
								</p>
								<div
									v-for="tournament of athlete.tournaments"
									:key="tournament.tournament_id">
									<div
										class="inline-flex ml-4 w-full"
										@click="
											() =>
												toogleInscription(
													tournament.tournament_id,
													athlete.athlete_id
												)
										">
										<p>
											{{ tournament.name }}
										</p>
										<a
											v-if="tournament.payment_comprovative_url"
											class="min-w-max link ml-auto"
											target="_blank"
											:href="
												'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
												tournament.payment_comprovative_url
											">
											{{ t("seePaymentComprovative") }}
										</a>
										<p v-else class="min-w-max ml-auto">
											{{ t("noPaymentComprovative") }}
										</p>
										<input
											v-model="tournament.accepted"
											value="true"
											type="checkbox"
											class="mt-1 ml-2 rounded-sm" />
									</div>
								</div>
							</div>
						</div>
					</div>
				</li>
			</ul>
		</div>
		<div class="bottom-4 sticky max-w-max mx-auto">
			<Button
				class="!px-20"
				:loading="showSpinningWheel"
				:message="t('acceptAthletes')"
				type="primary"
				@button-click="accept" />
		</div>

		<!-- List hidden to be copied -->
		<CopyAccepted
			:inscriptions-tournament="inscriptionsTournament"
			:inscriptions-athletes="inscriptionsAthletes"
			@copy-list-html-tournaments="(option) => (copyListHtmlTournaments = option)"
			@copy-list-html-athletes="(option) => (copyListHtmlAthletes = option)" />
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import CopyAccepted from "@/components/competition/partials/copyAccepted.vue";
import { ref, watch, onMounted } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam, getAthleteName } from "@/services/athlete.service.js";
import { useI18n } from "vue-i18n";
import toast from "@/toast";

const { t } = useI18n({ useScope: "global" });
const loading = ref(true);
const inscriptions = ref([]);
const copyListHtmlTournaments = ref(null);
const copyListHtmlAthletes = ref(null);
const inscriptionsTournament = ref([]);
const inscriptionsAthletes = ref([]);
const acceptAll = ref(false);
const showSpinningWheel = ref(false);
const competitionName = ref("");
const orderByTournament = ref(true);

const props = defineProps({
	// Competition ID
	competitionId: {
		type: String,
		required: true,
	},
	// Team ID
	teamId: {
		type: String,
		required: true,
	},
});

watch(
	() => acceptAll.value,
	(after) => {
		for (const inscription of inscriptions.value) {
			inscription.accepted = after;
		}
		for (const tournament of inscriptionsTournament.value) {
			for (const athleteTournament of tournament.athletes) {
				athleteTournament.accepted = after;
			}
		}
		for (const athlete of inscriptionsAthletes.value) {
			for (const tournamentAthlete of athlete.tournaments) {
				tournamentAthlete.accepted = after;
			}
		}
	}
);

onMounted(async () => {
	loading.value = true;
	try {
		const { data: dataCompetitionName } = await authApi.get(
			`competitions/name/${props.competitionId}`
		);
		const { data: inscriptionsList } = await authApi.get(
			`inscriptions?competition_id=${props.competitionId}&team_id=${props.teamId}&confirmed=true&limit=-1`
		);
		competitionName.value = dataCompetitionName;
		inscriptions.value = inscriptionsList.results;
		groupInscriptions();
	} catch (e) {
		errorHandling(e, true);
	} finally {
		loading.value = false;
	}
});

const groupInscriptions = () => {
	inscriptionsTournament.value = [];
	for (let inscription of inscriptions.value) {
		let indexTournament = inscriptionsTournament.value.findIndex(
			(a) => a.tournament_id == inscription.tournament_id
		);

		if (indexTournament === -1) {
			indexTournament = inscriptionsTournament.value.length;
			inscriptionsTournament.value.push({
				name: getTournamentName(inscription.tournament, t),
				athletes: [],
				tournament_id: inscription.tournament_id,
			});
		}
		inscriptionsTournament.value[indexTournament].athletes.push({
			athlete_id: inscription.athlete_competition_id,
			athlete: inscription.athlete_competition,
			accepted: inscription.accepted,
			payment_comprovative_url: inscription.payment_comprovative_url,
		});

		let indexAthlete = inscriptionsAthletes.value.findIndex(
			(a) => a.athlete_id == inscription.athlete_competition_id
		);

		if (indexAthlete === -1) {
			indexAthlete = inscriptionsAthletes.value.length;
			inscriptionsAthletes.value.push({
				name: getAthleteName(inscription.athlete_competition),
				tournaments: [],
				athlete_id: inscription.athlete_competition_id,
			});
		}
		inscriptionsAthletes.value[indexAthlete].tournaments.push({
			tournament_id: inscription.tournament_id,
			name: getTournamentName(inscription.tournament, t),
			accepted: inscription.accepted,
			payment_comprovative_url: inscription.payment_comprovative_url,
		});
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
	inscriptionsAthletes.value.sort((a, b) => {
		if (a.name < b.name) {
			return -1;
		}
		if (a.name > b.name) {
			return 1;
		}
		return 0;
	});
};

const accept = async () => {
	showSpinningWheel.value = true;
	let updateList = [];
	for (const inscription of inscriptions.value) {
		updateList.push({
			athlete_competition_id: inscription.athlete_competition_id,
			tournament_id: inscription.tournament_id,
			accepted: !!inscription.accepted,
		});
	}
	try {
		await authApi.put("inscriptions/accept/list", updateList);
		toast.success(t("athletesAccepted"));
	} catch (e) {
		console.log(e);
		errorHandling(e, true);
	} finally {
		showSpinningWheel.value = false;
	}
};

const toogleInscription = (tournament_id, athlete_id, acceptAll = false) => {
	for (const inscription of inscriptions.value) {
		if (
			inscription.tournament_id === tournament_id &&
			inscription.athlete_competition_id === athlete_id
		) {
			inscription.accepted = !inscription.accepted;
			break;
		}
	}
	for (const tournament of inscriptionsTournament.value) {
		if (tournament.tournament_id === tournament_id) {
			for (const tournamentAthlete of tournament.athletes) {
				if (tournamentAthlete.athlete_id === athlete_id) {
					tournamentAthlete.accepted = !tournamentAthlete.accepted;
					break;
				}
			}
			break;
		}
	}
	for (const athlete of inscriptionsAthletes.value) {
		if (athlete.athlete_id === athlete_id) {
			for (const athleteTournament of athlete.tournaments) {
				if (athleteTournament.tournament_id === tournament_id) {
					athleteTournament.accepted = !athleteTournament.accepted;
					break;
				}
			}
			break;
		}
	}
};

const copyList = () => {
	function listener(e) {
		e.clipboardData.setData(
			"text/html",
			orderByTournament.value
				? copyListHtmlTournaments.value.innerHTML
				: copyListHtmlAthletes.value.innerHTML
		);
		e.preventDefault();
	}
	document.addEventListener("copy", listener);
	document.execCommand("copy"); // Deprecated but found no alternative for rich text copy
	document.removeEventListener("copy", listener);
	toast.success(t("copied"));
};
</script>
