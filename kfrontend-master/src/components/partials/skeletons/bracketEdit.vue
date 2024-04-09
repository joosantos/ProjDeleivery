<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<div class="inline-flex w-full">
			<!-- All Athletes to add to the Tournament -->
			<div class="ml-auto w-80">
				<p class="font-bold text-xl text-center">{{ t("all") }}</p>
				<Loading v-if="loadingAthletes" />
				<div v-else>
					<div>
						<div class="flex flex-col my-2">
							<CustomInput
								:label="''"
								type="text"
								:name="'athleteSearch'"
								:option-selected="searchText"
								:error="''"
								@value-changed="
									(option) => {
										searchText = option;
										filterAthletes();
									}
								" />
						</div>
					</div>
					<div class="overflow-y-auto max-h-96">
						<div
							v-for="athlete of athletesCompetition"
							v-show="athlete.show"
							:key="athlete.id"
							class="text-center select-text">
							<p>
								{{ getAthleteNameTeam(athlete) }}
							</p>
						</div>
					</div>
				</div>
			</div>
			<Loading v-if="loadingTournament" />
			<div v-else class="max-w-max mx-auto w-full">
				<p class="ml-10 font-bold text-3xl mb-10">
					{{ getTournamentName(tournament, t) }}
				</p>
				<div v-if="tournament.matches.length == 0" />

				<!-- Edit Combat Tournaments -->
				<div v-else-if="tournament.category.category_type.name == 'Tournament'">
					<div class="max-w-max relative left-1/2 -translate-x-1/2">
						<div v-if="matches.length === 1" class="flex flex-col w-80">
							<SingleMatchEdit
								:match="matches[0]"
								@area="(option) => (matches[0].new_number_by_area = option)"
								@red="(option) => (matches[0].athlete_red.newName = option)"
								@blue="(option) => (matches[0].athlete_blue.newName = option)"
								@winner="(option) => (matches[0].winner.newName = option)" />
						</div>
						<div v-else-if="matches.length === 3">
							<div
								v-for="match in matches"
								:key="match.id"
								class="flex flex-col w-80">
								<SingleMatchEdit
									:match="match"
									@area="(option) => (match.new_number_by_area = option)"
									@red="(option) => (match.athlete_red.newName = option)"
									@blue="(option) => (match.athlete_blue.newName = option)"
									@winner="(option) => (match.winner.newName = option)" />
							</div>
						</div>
						<div v-else-if="matches.length >= 4">
							<div class="flex flex-row">
								<div v-if="matches.length >= 32" class="flex flex-col w-80">
									<p class="tournament-stage">
										{{ t("sixteen") }}
									</p>
									<SingleMatchEdit
										v-for="i in [...Array(16).keys()].map(
											(a) => a + matches.length - 32
										)"
										:key="matches[i].id"
										:match="matches[i]"
										@area="(option) => (matches[i].new_number_by_area = option)"
										@red="(option) => (matches[i].athlete_red.newName = option)"
										@blue="
											(option) => (matches[i].athlete_blue.newName = option)
										"
										@winner="
											(option) => (matches[i].winner.newName = option)
										" />
								</div>
								<div v-if="matches.length >= 16" class="w-80 justify-between">
									<p class="tournament-stage">
										{{ t("octo") }}
									</p>
									<div
										:class="[
											'flex flex-col w-80',
											matches.length === 32 && 'mt-32 space-y-[17.25rem]',
										]">
										<SingleMatchEdit
											v-for="i in [...Array(8).keys()].map(
												(a) => a + matches.length - 16
											)"
											:key="matches[i].id"
											:match="matches[i]"
											@area="
												(option) => (matches[i].new_number_by_area = option)
											"
											@red="
												(option) =>
													(matches[i].athlete_red.newName = option)
											"
											@blue="
												(option) =>
													(matches[i].athlete_blue.newName = option)
											"
											@winner="
												(option) => (matches[i].winner.newName = option)
											" />
									</div>
								</div>
								<div v-if="matches.length >= 8" class="w-80 justify-between">
									<p class="tournament-stage">
										{{ t("quarter") }}
									</p>
									<div
										:class="[
											'flex flex-col w-80',
											matches.length === 32 &&
												'mt-[25.25rem] space-y-[51.625rem]',
											matches.length === 16 && 'mt-32 space-y-[17.25rem]',
										]">
										<SingleMatchEdit
											v-for="i in [...Array(4).keys()].map(
												(a) => a + matches.length - 8
											)"
											:key="matches[i].id"
											:match="matches[i]"
											@area="
												(option) => (matches[i].new_number_by_area = option)
											"
											@red="
												(option) =>
													(matches[i].athlete_red.newName = option)
											"
											@blue="
												(option) =>
													(matches[i].athlete_blue.newName = option)
											"
											@winner="
												(option) => (matches[i].winner.newName = option)
											" />
									</div>
								</div>
								<div class="w-80 justify-between">
									<p class="tournament-stage">
										{{ t("semi") }}
									</p>
									<div
										:class="[
											'flex flex-col w-80',
											matches.length === 32 && 'mt-[60rem] space-y-[120rem]',
											matches.length === 16 &&
												'mt-[25.25rem] space-y-[51.625rem]',
											matches.length === 8 && 'mt-32 space-y-[17.25rem]',
										]">
										<SingleMatchEdit
											v-for="i in [matches.length - 4, matches.length - 3]"
											:key="matches[i].id"
											:match="matches[i]"
											@area="
												(option) => (matches[i].new_number_by_area = option)
											"
											@red="
												(option) =>
													(matches[i].athlete_red.newName = option)
											"
											@blue="
												(option) =>
													(matches[i].athlete_blue.newName = option)
											"
											@winner="
												(option) => (matches[i].winner.newName = option)
											" />
									</div>
								</div>
								<div class="flex flex-col w-80 my-auto">
									<div
										v-for="i in [matches.length - 2, matches.length - 1]"
										:key="matches[i].id">
										<p v-if="i === matches.length - 2" class="tournament-stage">
											{{ t("final") }}
										</p>
										<p v-else class="tournament-stage mt-10">
											{{ t("third") }}
										</p>
										<SingleMatchEdit
											:match="matches[i]"
											@area="
												(option) => (matches[i].new_number_by_area = option)
											"
											@red="
												(option) =>
													(matches[i].athlete_red.newName = option)
											"
											@blue="
												(option) =>
													(matches[i].athlete_blue.newName = option)
											"
											@winner="
												(option) => (matches[i].winner.newName = option)
											" />
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Edit List Tournaments -->
				<div v-else class="mt-10 max-w-max relative left-1/2 -translate-x-1/2">
					<SingleMatchEditList
						v-for="match in matches"
						:key="match.id"
						:match="match"
						@area="(option) => (match.new_number_by_area = option)"
						@red="(option) => (match.athlete_red.newName = option)"
						@points="(option) => (match.newPoints = option)" />
				</div>
			</div>

			<!-- Choose Bracket Size -->
			<div class="mr-auto w-80">
				<p class="font-bold text-xl text-center">{{ t("choose") }}</p>
				<select
					v-if="tournament.category.category_type.name == 'Tournament'"
					id="bracketSize"
					v-model="bracketSize"
					name="bracketSize"
					class="relative left-1/2 -translate-x-1/2 mt-2">
					<option value="0">0</option>
					<option value="1">1</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="8">8</option>
					<option value="16">16</option>
					<option value="32">32</option>
				</select>
				<div v-else>
					<CustomInput
						:label="''"
						type="text"
						:mask="'##'"
						:name="'bracketSize'"
						:option-selected="bracketSize"
						:error="''"
						@value-changed="
							(option) => {
								bracketSize = option;
							}
						" />
				</div>
				<div
					class="text-center border border-black cursor-pointer mt-4"
					@click="updateBracketSize">
					{{ t("confirm") }}
				</div>
			</div>
		</div>
		<div class="h-20"></div>
		<div class="max-w-max sticky bottom-4 left-1/2 -translate-x-1/2 z-10">
			<Button
				:message="t('update')"
				type="primary"
				:loading="buttonLoading"
				@button-click="update" />
		</div>
	</div>
</template>

<script setup>
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Loading from "@/components/partials/loading.vue";
import SingleMatchEdit from "@/components/partials/skeletons/singleMatchEdit.vue";
import SingleMatchEditList from "@/components/partials/skeletons/singleMatchEditList.vue";
import Button from "@/components/partials/button.vue";
import { ref } from "vue";
import { authApi, unauthApi } from "@/services/api";
import { useI18n } from "vue-i18n";
import toast from "@/toast.js";
import { getTournamentName } from "@/services/competition.service.js";
import { getAthleteNameTeam } from "@/services/athlete.service.js";

const props = defineProps({
	tournament: {
		type: Object,
		required: true,
	},
});

let { t } = useI18n();
let matches = ref([]);
let athletesCompetition = ref([]);
let searchText = ref("");
let tournament = ref(props.tournament);
let bracketSize = ref(tournament.value.matches.length);
let loading = ref(true);
let loadingTournament = ref(false);
let loadingAthletes = ref(true);
let buttonLoading = ref(false);

authApi
	.get(`competitions/${tournament.value.competition_id}/athlete-competition`)
	.then((response) => {
		for (let athlete of response.data) {
			athlete.show = true;
			athletesCompetition.value.push(athlete);
		}
		loadingAthletes.value = false;
	})
	.catch(() => {
		loadingAthletes.value = false;
		toast.error(t("error.athletes"));
	});

function filterAthletes() {
	if (searchText.value == "") {
		athletesCompetition.value.map((a) => (a.show = true));
		return;
	}
	athletesCompetition.value.map((a) => {
		let name = getAthleteNameTeam(a);
		if (name == null) {
			a.show = false;
			return;
		}
		a.show = name.toLowerCase().indexOf(searchText.value.toLowerCase()) != -1;
	});
}

function loadMatches() {
	for (let match of tournament.value.matches) {
		match.athlete_red = match.athlete_red || {};
		match.athlete_blue = match.athlete_blue || {};
		match.winner = match.winner || {};

		match.athlete_red.newName = getAthleteNameTeam(match.athlete_red);
		match.athlete_blue.newName = getAthleteNameTeam(match.athlete_blue);
		match.winner.newName = getAthleteNameTeam(match.winner);
		match.new_number_by_area = match.number_by_area;
		matches.value.push(match);
	}
	matches.value.sort((a, b) => {
		return a.number - b.number;
	});
	loading.value = false;
}
loadMatches();

function getTournament() {
	loadingTournament.value = true;
	unauthApi
		.get("tournaments/" + tournament.value.id)
		.then((response) => {
			matches.value = [];
			tournament.value = response.data;
			loadMatches();
			toast.success(t("successUpdate"));
			loadingTournament.value = false;
			loading.value = false;
		})
		.catch(() => {
			loadingTournament.value = false;
			loading.value = false;
			toast.error(t("error.tournament"));
		});
}

function getMatchUpdateObject(match) {
	let updateObj = {
		id: match.id,
		athlete_red_id: match.athlete_red_id || null,
		athlete_blue_id: match.athlete_blue_id || null,
		winner_id: match.winner_id || null,
		number_by_area: match.number_by_area || null,
		toUpdate: false,
	};

	// See if athlete red is to be updated and save it's ID
	if (match.athlete_red.newName != getAthleteNameTeam(match.athlete_red)) {
		if (!match.athlete_red.newName || !match.athlete_red.newName.trim())
			updateObj.athlete_red_id = null;
		else {
			let athlete = athletesCompetition.value.find(
				(a) => getAthleteNameTeam(a) == match.athlete_red.newName
			);
			if (athlete == null) {
				return null;
			}
			updateObj.athlete_red_id = athlete.id;
		}
		updateObj.toUpdate = true;
	}

	// See if athlete blue is to be updated and save it's ID
	if (match.athlete_blue.newName != getAthleteNameTeam(match.athlete_blue)) {
		if (!match.athlete_blue.newName || !match.athlete_blue.newName.trim())
			updateObj.athlete_blue_id = null;
		else {
			let athlete = athletesCompetition.value.find(
				(a) => getAthleteNameTeam(a) == match.athlete_blue.newName
			);
			if (athlete == null) {
				return null;
			}
			updateObj.athlete_blue_id = athlete.id;
		}
		updateObj.toUpdate = true;
	}

	// See if winner is to be updated and save it's ID
	if (match.winner.newName != getAthleteNameTeam(match.winner)) {
		if (!match.winner.newName || !match.winner.newName.trim()) updateObj.winner_id = null;
		else {
			let athlete = athletesCompetition.value.find(
				(a) => getAthleteNameTeam(a) == match.winner.newName
			);
			if (athlete == null) {
				return null;
			}
			updateObj.winner_id = athlete.id;
		}
		updateObj.toUpdate = true;
	}

	// See if match_number is to be updated and save it's number
	if (match.new_number_by_area != match.number_by_area) {
		updateObj.toUpdate = true;
		updateObj.number_by_area = match.new_number_by_area || null;
	}
	return updateObj;
}

function update() {
	buttonLoading.value = true;
	let promises = [];
	if (tournament.value.category.category_type.name == "Tournament") {
		let matchesToUpdate = [];
		let errorUpdate = false;
		for (let match of matches.value) {
			let updateMatch = getMatchUpdateObject(match);
			if (updateMatch == null) {
				toast.error(t("error.updateMatch", { count: 1 }));
				errorUpdate = true;
				continue;
			}
			if (updateMatch.toUpdate) {
				updateMatch.id = match.id;
				matchesToUpdate.push(updateMatch);
			}
		}
		if (errorUpdate) {
			buttonLoading.value = false;
			return;
		}
		for (let match of matchesToUpdate) {
			if (!match.toUpdate) continue;
			promises.push(authApi.put(`matches/${match.id}`, match));
		}
	} else {
		let matchesToUpdate = [];
		for (let match of matches.value) {
			let updateMatch = getMatchUpdateObject(match);
			if (updateMatch == null) {
				toast.error(t("error.updateMatch", { count: 1 }));
				buttonLoading.value = false;
				return;
			}
			if (updateMatch.toUpdate) {
				updateMatch.id = match.id;
				matchesToUpdate.push(updateMatch);
			}
		}

		for (let match of matchesToUpdate) {
			if (!match.toUpdate) continue;
			promises.push(authApi.put(`matches/${match.id}`, match));
		}
	}

	Promise.all(promises)
		.then(() => {
			getTournament();
			buttonLoading.value = false;
		})
		.catch(() => {
			loading.value = false;
			buttonLoading.value = false;
			toast.error(t("error.update"));
		});
}

function updateBracketSize() {
	loading.value = true;
	if (tournament.value.matches.length == bracketSize.value) {
		toast.error(t("error.bracketSize"));
		loading.value = false;
		return;
	}

	let promises = [];
	if (tournament.value.matches.length > bracketSize.value) {
		let numberToRemove = tournament.value.matches.length - Number(bracketSize.value);
		for (let i = 0; i < numberToRemove; i++) {
			let matchIndex = tournament.value.matches.findIndex(
				(a) => a.number == tournament.value.matches.length - i
			);
			if (matchIndex === -1) {
				toast.error(t("error.notFound", { count: tournament.value.matches.length - i }));
				return;
			}
			promises.push(authApi.delete("matches/" + tournament.value.matches[matchIndex].id));
		}
	} else {
		let numberToAdd = Number(bracketSize.value) - tournament.value.matches.length;
		for (let i = 0; i < numberToAdd; i++) {
			promises.push(
				authApi.post("tournaments/" + tournament.value.id + "/matches/single", {
					number: tournament.value.matches.length + i + 1,
				})
			);
		}
	}
	Promise.all(promises)
		.then(() => {
			getTournament();
		})
		.catch(() => {
			loading.value = false;
			toast.error(t("error.bracket"));
		});
}
</script>

<i18n>
{
	"en_GB": {
		"all": "Competition Athletes",
		"choose": "Chose Bracket size",
		"confirm": "Confirm",
		"octo": "Round of 16",
		"sixteen": "Round of 32",
		"quarter": "Quarter-finals",
		"semi": "Semi-finals",
		"final": "Final",
		"winner": "Winner",
		"update": "Update Tournament",
		"third": "Third Place Qualification",
		"addAthlete": "Add new Athlete",
		"error": {
			"athletes": "Couldn't get the athletes",
			"updateMatch": "Invalid values for match {count}",
			"emptyMatch": "The match {count} has no athletes",
			"notFound": "The match {count} was not found",
			"update": "Error updating the matches",
			"bracketSize": "The bracket is already of the selected size",
			"bracket": "Wasn't possible to update the bracket size",
			"tournament": "Wasn't possible to recive the tournament"
		},
		"successUpdate": "Matches Updated",
		"open": "Open",
		"masc": "Masculine",
		"fem": "Feminine",
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
		"all": "Atletas da Competição",
		"choose": "Escolher tamanho da Bracket",
		"confirm": "Confirmar",
		"octo": "Oitavos de final",
		"sixteen": "Dezaseis avos de final",
		"quarter": "Quartos de final",
		"semi": "Semi-finais",
		"final": "Final",
		"winner": "Vencedor",
		"update": "Atualizar torneio",
		"third": "Disputa do terceiro lugar",
		"addAthlete": "Adicionar um novo atleta",
		"error": {
			"athletes": "Não foi possível receber a informação dos atletas",
			"updateMatch": "Valores inválidos para o combate {count}",
			"emptyMatch": "O combate {count} não tem atletas",
			"update": "Erro a atualizar os combates",
			"bracketSize": "A Bracket já é do tamanho selecionado",
			"bracket": "Não foi possível atualizar o tamanho da bracket",
			"tournament": "Não foi possível receber o torneio"
		},
		"successUpdate": "Combates atualizados",
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
