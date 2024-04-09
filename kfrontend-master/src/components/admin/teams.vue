<template>
	<div>
		<EditTeamModal
			:open="openEdit"
			:team-id="editID"
			@close="
				editID = '';
				openEdit = false;
				getTeams();
			" />
		<ConfirmationModal
			:open="openDelete"
			:title="t('delete.title')"
			:message="t('delete.message', { name: deleteName })"
			:button-text="t('delete.button')"
			:loading="showDeleteLoading"
			:show-x="showDeleteX"
			@close="closeDeleteModal"
			@deleted="deleteTeam" />
		<Loading v-if="loading" :size="10" />
		<div v-else>
			<form
				class="md:inline-flex md:flex-row flex flex-col space-y-4 md:space-y-0 md:space-x-4 relative left-1/2 -translate-x-1/2">
				<CustomInput
					type="text"
					:label="t('filter.name')"
					:name="'filterByName'"
					:option-selected="filters.name"
					:error="''"
					@value-changed="
						(option) => {
							filters.name = option;
							filterTeams();
						}
					" />
				<CustomInput
					type="text"
					:label="t('filter.abr')"
					:name="'filterByAbr'"
					:option-selected="filters.abr"
					:error="''"
					@value-changed="
						(option) => {
							filters.abr = option;
							filterTeams();
						}
					" />
				<CustomInput
					type="text"
					:label="t('filter.coach')"
					:name="'filterByCoach'"
					:option-selected="filters.coach"
					:error="''"
					@value-changed="
						(option) => {
							filters.coach = option;
							filterTeams();
						}
					" />
				<div class="mx-auto relative md:top-5">
					<Trash
						:text="t('filter.clear')"
						@button-click="
							filters.name = '';
							filters.abr = '';
							filters.coach = '';
						" />
				</div>
			</form>
			<div class="mt-4 w-60 mx-auto">
				<Button
					:message="t('createAthlete')"
					:type="'success'"
					:pill="true"
					@button-click="
						router.push({ name: 'Athlete Details', params: { athleteId: '0' } })
					" />
			</div>
			<div class="space-y-4 max-w-max mt-8 mx-auto">
				<div
					v-for="team of teams"
					v-show="team.show"
					:key="team.id"
					class="flex flex-col bg-blue-100 px-8 pb-2 pt-4 rounded-lg border border-blue-700">
					<div class="justify-between inline-flex">
						<p class="text-left text-lg font-medium">
							{{ `${team.name} (${team.abbreviation})` }}
						</p>
						<router-link
							v-if="team.id != '1' && team?.coach?.athlete_id != null"
							:to="{
								name: 'Athlete Details',
								params: { athleteId: team.coach.athlete_id },
							}"
							class="text-right ml-2 link">
							{{ team.coach.name }}
						</router-link>
						<p v-else class="text-right ml-2">
							{{ team.coach.name }}
						</p>
					</div>
					<p v-if="team.federation_number" class="text-left text-lg font-medium">
						{{ t("federationNumberNumber", { number: team.federation_number }) }}
					</p>
					<div
						class="md:inline-flex md:flex-row flex flex-col space-y-4 md:space-y-0 md:space-x-4 max-w-max mt-4 relative left-1/2 -translate-x-1/2">
						<router-link
							:to="{ name: 'Athletes By Team', params: { teamId: team.id } }"
							class="px-4 py-2 rounded-full border border-blue-500 bg-blue-100 cursor-pointer min-w-[10rem] hover:bg-blue-200 hover:border-blue-700">
							<p class="text-center">{{ t("seeAthletes") }}</p>
						</router-link>
						<router-link
							:to="{ name: 'Admin Team View', params: { teamId: team.id } }"
							class="px-4 py-2 rounded-full border border-blue-500 bg-blue-100 cursor-pointer min-w-[10rem] hover:bg-blue-200 hover:border-blue-700">
							<p class="text-center">{{ t("manageTeam") }}</p>
						</router-link>
						<router-link
							v-if="team.id != '1'"
							:to="{ name: 'Team Details', params: { teamId: team.id } }"
							class="px-4 py-2 rounded-full border border-green-500 bg-green-100 cursor-pointer min-w-[10rem] hover:bg-green-200 hover:border-green-700">
							<p class="text-center">{{ t("seeInsurances") }}</p>
						</router-link>
						<button
							v-if="team.id != '1'"
							class="px-4 py-2 rounded-full border border-yellow-500 bg-yellow-100 cursor-pointer min-w-[10rem] hover:bg-yellow-200 hover:border-yellow-700"
							@click.prevent="
								editID = team.id;
								openEdit = true;
							">
							<p class="text-center">{{ t("editTeam") }}</p>
						</button>
						<button
							v-if="team.id != '1'"
							class="px-4 py-2 rounded-full border border-red-500 bg-red-100 cursor-pointer min-w-[10rem] hover:bg-red-200 hover:border-red-700"
							@click.prevent="
								deleteID = team.id;
								deleteName = `${team.name} (${team.abbreviation})`;
								openDelete = true;
							">
							<p class="text-center">{{ t("deleteTeam") }}</p>
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import CustomInput from "@/components/partials/inputs/customInput.vue";
import ConfirmationModal from "@/components/partials/messages/confirmation.vue";
import Trash from "@/components/partials/inputs/trash.vue";
import Loading from "@/components/partials/loading.vue";
import Button from "@/components/partials/button.vue";
import EditTeamModal from "@/components/admin/modals/editTeam.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";
import router from "@/router";
import toast from "@/toast.js";

let { t } = useI18n();
let teams = ref([]);
let loading = ref(true);
let openEdit = ref(false);
let editID = ref("");
let openDelete = ref(false);
let deleteID = ref("");
let deleteName = ref("");
let showDeleteLoading = ref(false);
let showDeleteX = ref(false);
let filters = ref({
	name: "",
	abr: "",
	coach: "",
});

function getTeams() {
	loading.value = true;
	authApi
		.get("teams")
		.then((response) => {
			teams.value = response.data;
			teams.value.unshift({
				name: t("noTeamAthletes"),
				abbreviation: "AWT",
				id: "1",
				coach: { name: "" },
			});
			filterTeams();
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error);
		});
}
getTeams();

function filterTeams() {
	for (let team of teams.value) {
		team.show = true;
		if (
			team.name.toLocaleUpperCase().indexOf(filters.value.name.toLocaleUpperCase()) == -1 ||
			team.abbreviation.toLocaleUpperCase().indexOf(filters.value.abr.toLocaleUpperCase()) ==
				-1 ||
			team.coach.name.toLocaleUpperCase().indexOf(filters.value.coach.toLocaleUpperCase())
		)
			team.show = false;
	}
}

function closeDeleteModal() {
	deleteID.value = "";
	deleteName.value = "";
	openDelete.value = false;
	getTeams();
}

function deleteTeam() {
	showDeleteLoading.value = true;
	showDeleteX.value = false;
	authApi
		.delete(`teams/${deleteID.value}`)
		.then(() => {
			showDeleteLoading.value = false;
			toast.success(t("teamDeleted", { name: deleteName.value }));
			closeDeleteModal();
		})
		.catch((error) => {
			showDeleteLoading.value = false;
			showDeleteX.value = true;
			errorHandling(error);
		});
}
</script>

<i18n>
{
	"en_GB": {
		"manageTeam": "Manage Team",
		"filter": {
			"name": "Filter by Name",
			"abr": "Filter by Abbreviation",
			"coach": "Filter by Coach",
			"clear": "Clear Filters",
		},
		"delete": {
			"title": "Delete Team",
			"message": "Are you sure you want to delete the team {name}?",
			"button": "Delete"
		},
		"createAthlete": "Create new Athlete",
		"seeAthletes": "See Athletes",
		"editTeam": "Edit Team",
		"deleteTeam": "Delete Team",
		"teamDeleted": "Team {name} Deleted",
		"noTeamAthletes": "Athletes Without Team",
		"seeInsurances": "Insurances",
	},
	"pt_PT": {
		"manageTeam": "Gerir equipa",
		"filter": {
			"name": "Filtrar por Nome",
			"abr": "Filtrar por Abreviatura",
			"coach": "Filtrar por Treinador",
			"clear": "Limpar Filtros"
		},
		"createAthlete": "Create new Athlete",
		"seeAthletes": "Ver Atletas",
		"editTeam": "Editar Equipa",
		"deleteTeam": "Apagar Equipa",
		"teamDeleted": "Equipa {name} Apagada",
		"noTeamAthletes": "Atletas Sem Equipa",
		"seeInsurances": "Seguros",
	}
}
</i18n>
