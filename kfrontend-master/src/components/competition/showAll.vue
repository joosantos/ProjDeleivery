<template>
	<div class="ml-6 mt-2 mb-6 w-60">
		<router-link
			v-if="store.getters.getUserRole == 'ADMIN'"
			:to="{ name: 'Competition Create' }">
			<Button
				:message="t('create')"
				type="primary"
				:pill="true"
				:outline="true"
				@button-click="null" />
		</router-link>
	</div>
	<div class="ml-6 mt-2 mb-6 w-60">
		<router-link v-if="store.getters.getUserRole == 'COACH'" :to="{ name: 'Coach Dashboard' }">
			<Button
				:message="t('inscriptions')"
				type="primary"
				:pill="true"
				:outline="true"
				@button-click="null" />
		</router-link>
	</div>
	<div class="p-6 py-0 text-center text-black">
		<div class="text-3xl font-bold text-left">{{ t("competition.title") }}</div>
		<div class="bg-gray-100 border border-gray-300 rounded-xl mt-2">
			<Loading v-if="loading" :size="10" />
			<h1 v-if="!loading && !competitions.length" class="font-bold text-xl py-4">
				{{ t("noCompetitions") }}
			</h1>
			<div v-else>
				<div
					v-for="competition of competitions"
					:key="competition.id"
					class="w-full px-4 py-2">
					<div class="bg-blue-100 rounded-xl py-1 px-2 border border-blue-300">
						<router-link
							class="mt-2 flex flex-col md:inline-flex md:flex-row justify-between w-full cursor-pointer hover:bg-blue-200 rounded-xl px-4 py-1 group"
							:to="{
								name: 'Show Competition',
								params: { competition: competition.id },
							}">
							<h1 class="text-2xl font-semibold md:text-left">
								{{ competition.name }}
							</h1>
							<p
								class="mt-1 text-blue-500 group-hover:text-blue-800 group-hover:font-medium cursor-pointer select-none">
								{{ t("table.show") }}
							</p>
						</router-link>
						<div
							class="flex flex-col md:inline-flex md:flex-row justify-between w-full">
							<div
								v-if="competition.name != 'DEFAULTS'"
								:class="[
									'grid grid-cols-2 max-w-max gap-y-2 mt-2 mx-auto md:mx-0',
									store.getters.getUser?.user_role?.role?.name == 'ADMIN'
										? 'grid-rows-2'
										: 'grid-rows-1',
								]">
								<div class="inline-flex w-full">
									<div class="w-12">
										<UserIcon
											class="h-7 w-7 text-gray-800 ml-1 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{ t("table.athletes", { count: competition.athletes }) }}
									</h3>
								</div>
								<div
									v-if="store.getters.getUser?.user_role?.role?.name == 'ADMIN'"
									class="inline-flex w-full">
									<div class="w-12">
										<TournamentBracket
											class="h-8 w-8 text-gray-800 ml-1 -mt-0.5 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{
											t("table.tournaments", {
												count: competition.tournaments,
											})
										}}
									</h3>
								</div>
								<div class="inline-flex w-full">
									<div class="w-12">
										<PunchFist
											class="h-10 w-10 text-gray-800 ml-1 -mt-1.5 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{ t("table.matches", { count: competition.matches }) }}
									</h3>
								</div>
								<div
									v-if="store.getters.getUser?.user_role?.role?.name == 'ADMIN'"
									class="inline-flex w-full">
									<div class="w-12">
										<DirectWinner
											class="h-8 w-8 text-gray-800 ml-1 -mt-0.5 relative left-1/2 -translate-x-1/2" />
									</div>
									<h3 class="text-left font-normal text-lg ml-2">
										{{
											t("table.direct", { count: competition.direct_winners })
										}}
									</h3>
								</div>
							</div>
							<div v-else />
							<div class="w-50 flex flex-col gap-y-2 mt-2">
								<LinkTable
									v-if="competition.name != 'DEFAULTS'"
									:router-to="{
										name: 'Statistics',
										params: { competition: competition.id },
									}"
									:text="t('table.statistics')" />
								<LinkTable
									v-if="store.getters.getUser?.user_role?.role?.name == 'ADMIN'"
									:router-to="{
										name: 'Competition Details',
										params: { competitionId: competition.id },
									}"
									:text="t('table.details')" />
								<LinkTable
									v-if="
										store.getters.getUser?.user_role?.role?.name == 'ADMIN' &&
										competition.name != 'DEFAULTS'
									"
									:router-to="{
										name: 'Order Tournaments',
										params: { competitionId: competition.id },
									}"
									:text="t('table.order')" />
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import Loading from "@/components/partials/loading.vue";
import LinkTable from "@/components/competition/partials/linkTable.vue";
import { UserIcon } from "@heroicons/vue/24/solid";
import PunchFist from "@/components/icons/punchFist.vue";
import TournamentBracket from "@/components/icons/tournamentBracket.vue";
import DirectWinner from "@/components/icons/directWinner.vue";
import { ref } from "vue";
import { authApi, unauthApi } from "@/services/api";
import store from "@/store";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

let competitions = ref([]);
let loading = ref(true);

let request =
	store.getters.getUser == null
		? unauthApi.get("competitions/all")
		: authApi.get("competitions/all");
request
	.then((response) => {
		response.data.sort((a, b) => {
			if (a.name == "DEFAULTS") return -1;
			if (b.name == "DEFAULTS") return 1;
			if (new Date(a.competition_start) < new Date()) return 1;
			if (new Date(b.competition_start) < new Date()) return -1;
			return new Date(a.competition_start) - new Date(b.competition_start);
		});
		competitions.value = response.data;
		loading.value = false;
	})
	.catch(() => {
		toast.error(t("competition.notLoaded"));
		loading.value = false;
	});
</script>

<i18n>
{
  	"en_GB": {
		"updateTeams": "Update Teams",
		"create": "Create Competition",
		"inscriptions": "Go To Inscriptions",
		"noCompetitions": "No Competitions To Show",
		"competition": {
			"notLoaded": "Wasn't possible to load competitions",
			"title": "Competitions"
		},
		"table": {
			"tournaments": "{count} Tournaments",
			"athletes": "{count} Athletes",
			"show": "Show Competition",
			"statistics": "Show Statistics",
			"order": "Order tournaments",
			"matches": "{count} Matches",
			"direct": "{count} Direct Winners",
			"details": "Details"
		}
	},
	"pt_PT": {
		"updateTeams": "Atualizar Equipas",
		"create": "Criar nova Competição",
		"inscriptions": "Ir Para as Inscrições",
		"noCompetitions": "Sem Competições Para Mostrar",
		"competition": {
			"notLoaded": "Não foi possível carregar as competições",
			"title": "Competições"
		},
		"table": {
			"tournaments": "{count} Torneios",
			"athletes": "{count} Atletas",
			"show": "Mostrar competição",
			"statistics": "Mostrar estatísticas",
			"order": "Ordenar Torneios",
			"matches": "{count} Combates",
			"direct": "{count} Vencedores Diretos",
			"details": "Detalhes"
		}
	}
}
</i18n>
