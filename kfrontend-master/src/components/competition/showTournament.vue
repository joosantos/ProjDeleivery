<template>
	<Loading v-if="tournament == null" />
	<div v-else>
		<div v-if="tournament.matches.length == 0" class="w-screen print:hidden">
			<div
				class="mx-auto xl:grid xl:grid-cols-6 flex flex-col w-[90vh] xl:w-auto xl:mx-4 print:hidden mt-1 gap-y-4 xl:gap-y-0 xl:gap-x-4">
				<Button
					v-if="
						store.getters.getUserRole === 'ADMIN' && tournament.second_place_id == null
					"
					:message="t('recreate')"
					type="primary"
					:pill="true"
					:show-loading="recreateShowLoading"
					:show-x="recreateShowX"
					@button-click="recreateMatches" />
				<Button
					v-if="store.getters.getUserRole === 'ADMIN' && tournament.day != null"
					:message="
						t('renumber', {
							area: tournament.area,
							day: tournament.day,
							morning: tournament.morning
								? t('morning').toLowerCase()
								: t('afternoon').toLowerCase(),
						})
					"
					type="primary"
					:pill="true"
					:show-loading="renumberShowLoading"
					:show-x="renumberShowX"
					@button-click="renumber" />
			</div>
		</div>
		<div v-if="tournament.matches.length == 0" class="max-w-xl mx-auto mt-60">
			<p class="font-medium text-3xl">
				{{ t("noAthletes") }}
			</p>
			<div class="relative mt-16">
				<Button
					:message="t('return')"
					type="primary"
					:pill="true"
					@button-click="
						router.push({
							name: 'Show Competition',
							params: {
								competition: tournament.competition_id,
							},
						})
					" />
			</div>
		</div>
		<div
			v-else-if="tournament.category.category_type.name == 'Tournament'"
			:class="[
				'absolute top-0 left-0',
				tournament.matches.length > 50
					? 'scale-x-50 scale-y-50 -translate-x-1/4 -translate-y-1/4'
					: '',
			]">
			<Loading v-if="loadingTournament" />
			<div v-else>
				<div class="w-screen print:hidden">
					<div
						class="mx-auto xl:grid xl:grid-cols-6 flex flex-col w-[90vh] xl:w-auto xl:mx-4 print:hidden mt-2 gap-y-4 xl:gap-y-0 xl:gap-x-4">
						<Button
							v-if="
								(store.getters.getUserRole === 'ADMIN' ||
									store.getters.getUserRole === 'PODIUM') &&
								tournament.matches.length !== 0 &&
								tournament.first_place_id != null
							"
							:message="t('print')"
							type="primary"
							:pill="true"
							@button-click="printDiplomas" />
						<Button
							v-if="store.getters.getUserRole === 'ADMIN'"
							:message="t('recreate')"
							type="primary"
							:pill="true"
							:show-loading="recreateShowLoading"
							:show-x="recreateShowX"
							@button-click="recreateMatches" />
						<Button
							v-if="store.getters.getUserRole === 'ADMIN'"
							:message="t('printPDF')"
							type="primary"
							:pill="true"
							@button-click="printToPdf" />
						<Button
							v-if="store.getters.getUserRole === 'ADMIN' && tournament.day != null"
							:message="
								t('renumber', {
									area: tournament.area,
									day: tournament.day,
									morning: tournament.morning
										? t('morning').toLowerCase()
										: t('afternoon').toLowerCase(),
								})
							"
							type="primary"
							:pill="true"
							:show-loading="renumberShowLoading"
							:show-x="renumberShowX"
							@button-click="renumber" />
					</div>
				</div>
				<Bracket2 v-if="tournament.matches.length < 2" :tournament="tournament" />
				<Bracket3 v-else-if="tournament.matches.length < 4" :tournament="tournament" />
				<Bracket4 v-else-if="tournament.matches.length < 5" :tournament="tournament" />
				<Bracket8 v-else-if="tournament.matches.length < 9" :tournament="tournament" />
				<Bracket16 v-else-if="tournament.matches.length < 17" :tournament="tournament" />
				<Bracket32 v-else-if="tournament.matches.length < 33" :tournament="tournament" />
				<p v-else>
					{{ t("tournament.matchesError") }}
				</p>
			</div>
		</div>
		<div v-else class="absolute inset-0">
			<div class="inline-flex ml-4 gap-x-4 mt-4 print:hidden">
				<div class="max-w-max">
					<Button
						v-if="store.getters.getUserRole === 'ADMIN'"
						:message="t('recreate')"
						type="primary"
						:pill="true"
						:show-loading="recreateShowLoading"
						:show-x="recreateShowX"
						@button-click="recreateMatches" />
				</div>
				<div class="max-w-max">
					<Button
						v-if="store.getters.getUserRole === 'ADMIN' && tournament.day != null"
						:message="
							t('renumber', {
								area: tournament.area,
								day: tournament.day,
								morning: tournament.morning
									? t('morning').toLowerCase()
									: t('afternoon').toLowerCase(),
							})
						"
						type="primary"
						:pill="true"
						:show-loading="renumberShowLoading"
						:show-x="renumberShowX"
						@button-click="renumber" />
				</div>
				<div class="max-w-max">
					<Button
						v-if="store.getters.getUserRole === 'ADMIN'"
						:message="t('printPDF')"
						type="primary"
						:pill="true"
						@button-click="printToPdf" />
				</div>
				<div class="max-w-max">
					<Button
						v-if="
							(store.getters.getUserRole === 'ADMIN' ||
								store.getters.getUserRole === 'PODIUM') &&
							tournament.matches.length !== 0 &&
							tournament.first_place_id != null
						"
						:message="t('print')"
						type="primary"
						:pill="true"
						@button-click="printDiplomas" />
				</div>
			</div>
			<ListTournament :tournament="tournament" />
		</div>
	</div>
</template>

<script setup>
import Bracket2 from "@/components/partials/skeletons/bracket2.vue";
import Bracket3 from "@/components/partials/skeletons/bracket3.vue";
import Bracket4 from "@/components/partials/skeletons/bracket4.vue";
import Bracket8 from "@/components/partials/skeletons/bracket8.vue";
import Bracket16 from "@/components/partials/skeletons/bracket16.vue";
import Bracket32 from "@/components/partials/skeletons/bracket32.vue";
import ListTournament from "@/components/partials/skeletons/listTournament.vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import { unauthApi, authApi } from "@/services/api";
import { ref } from "vue";
import toast, { genericError } from "@/toast.js";
import store from "@/store";
import router from "@/router";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

store.commit("setShowNavBar", false);
store.commit("setShowMargins", false);

const props = defineProps({
	// ID of the tournament
	tournament: {
		type: String,
		required: true,
	},
});

let tournament = ref(null);
let loadingTournament = ref(false);
let recreateShowLoading = ref(false);
let recreateShowX = ref(false);
let renumberShowLoading = ref(false);
let renumberShowX = ref(false);

function getTournament() {
	loadingTournament.value = true;
	unauthApi
		.get("tournaments/" + props.tournament)
		.then((response) => {
			tournament.value = response.data;

			loadingTournament.value = false;
			if (tournament.value.matches.length == 0) {
				store.commit("setShowNavBar", true);
				store.commit("setShowMargins", true);
			}
		})
		.catch(() => {
			toast.error(t("tournament.notLoaded"));
		});
}
getTournament();
function printDiplomas() {
	if (tournament.value.first_place_id != null) {
		let routeData = router.resolve({
			name: "Diploma 1",
			params: { tournament: props.tournament },
		});
		window.open(routeData.href, "_blank");
	}
}
function printToPdf() {
	print();
}
function recreateMatches() {
	recreateShowLoading.value = true;
	recreateShowX.value = false;

	authApi
		.post(`tournaments/${props.tournament}/recreate`)
		.then(() => {
			getTournament();
			toast.success(t("recreated"));
		})
		.catch((error) => {
			console.log(error);
			genericError();
			recreateShowX.value = true;
		})
		.finally(() => {
			recreateShowLoading.value = false;
		});
}

function renumber() {
	renumberShowLoading.value = true;
	renumberShowX.value = false;

	authApi
		.post(
			`competitions/${tournament.value.competition_id}/tournaments/renumber?day=${tournament.value.day}&morning=${tournament.value.morning}&area=${tournament.value.area}`
		)
		.then(() => {
			getTournament();
			toast.success(t("renumbered"));
		})
		.catch((error) => {
			console.log(error);
			genericError();
			renumberShowX.value = true;
		})
		.finally(() => {
			renumberShowLoading.value = false;
		});
}
</script>

<i18n>
{
	"en_GB": {
		"print": "Print diplomas",
		"recreate": "Recreate matches",
		"renumber": "Renumber matches for the day {day}, area {area}, {morning}",
		"recreated": "Matches recreated!",
		"renumbered": "Matches renumbered!",
		"printTournament": "Print Tournament",
		"day": "Day {count}",
		"morning": "Morning",
		"afternoon": "Afternoon",
		"return": "Return",
		"noAthletes": "This tournament has no athletes signed up",
		"tournament": {
			"notLoaded": "Wasn't possible to load the tournament",
			"matchesError": "The tournament has more than 32 matches"
		},
		"printPDF": "Print to PDF"
	},
	"pt_PT": {
		"print": "Imprimir diplomas",
		"recreate": "Recriar provas",
		"renumber": "Recriar provas para o dia {day}, area {area}, {morning}",
		"recreated": "Provas recriadas!",
		"renumbered": "Provas renumeradas!",
		"day": "Dia {count}",
		"morning": "Manhã",
		"afternoon": "Tarde",
		"return": "Voltar",
		"noAthletes": "Este torneio não tem atletas inscritos",
		"tournament": {
			"notLoaded": "Não foi possível carregar o torneio",
			"matchesError": "Este torneio tem mais de 32 combates"
		},
		"printPDF": "Imprimir para PDF"
	}
}
</i18n>
