<template>
	<div>
		<TeamModal
			:open="openTeamModal"
			:team-id="teamId"
			@created="getTeams"
			@updated="getTeams"
			@close="openTeamModal = false" />
		<Loading v-if="loading" :size="10" />
		<div v-else>
			<div class="flex flex-col p-6 max-w-max mx-auto">
				<div class="inline-flex relative">
					<p class="text-center mx-auto text-3xl font-medium text-blue-900 mb-4">
						{{ t("myTeams") }}
					</p>
					<div class="absolute right-4 bottom-0 w-60 ml-auto mb-4 top-14">
						<Button
							:message="t('createTeam')"
							type="primary"
							:pill="true"
							@button-click="
								teamId = '';
								openTeamModal = true;
							" />
					</div>
				</div>
				<div class="overflow-x-auto md:overflow-x-visible min-w-max md:min-w-fit mt-14">
					<div
						:class="[
							'grid grid-cols-6 border-2 rounded-3xl border-blue-700 text-center space-x-4 divide-x-2 divide-blue-700 text-lg font-medium rounded-b-none',
						]">
						<p class="col-span-2 p-2">
							{{ t("association") }}
						</p>
						<p class="col-span-2 p-2">
							{{ t("name") }}
						</p>
						<p class="col-span-1 p-2 w-full">
							{{ t("abbreviation") }}
						</p>
						<p class="col-span-1 p-2">
							{{ t("actions") }}
						</p>
					</div>
					<div
						v-if="teams.length == 0"
						class="grid grid-cols-6 border-2 border-t-0 border-blue-700 rounded-3xl rounded-t-none text-center space-x-4 divide-x-2 divide-blue-700">
						<div class="col-span-6 p-2 font-medium text-xl">{{ t("noTeams") }}</div>
					</div>
					<div
						v-for="(team, index) of teams"
						:key="team.id"
						:class="[
							'grid grid-cols-6 border-2 border-t-0 border-blue-700 rounded-t-none text-center space-x-4 divide-x-2 divide-blue-700',
							index == teams.length - 1 ? 'rounded-3xl' : '',
						]">
						<div class="col-span-2 px-2 py-1">
							{{ team.association }}
						</div>
						<div class="col-span-2 px-2 py-1">
							{{ team.name }}
						</div>
						<div class="col-span-1 px-2 py-1">
							{{ team.abbreviation }}
						</div>
						<div
							class="col-span-1 px-2 py-1 inline-flex mx-auto justify-center space-x-4">
							<Tooltip :text="t('edit')">
								<PencilIcon
									class="h-6 w-6 bg-yellow-200 text-yellow-600 rounded-full p-0.5 cursor-pointer"
									@click="
										teamId = team.id;
										openTeamModal = true;
									" />
							</Tooltip>
							<Tooltip :text="t('manageTeam')">
								<SquaresPlusIcon
									class="h-6 w-6 bg-green-200 text-green-600 rounded-full p-0.5 cursor-pointer"
									@click="
										router.push({
											name: 'Team View',
											params: { teamId: team.id },
										})
									" />
							</Tooltip>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import TeamModal from "@/components/coach/modals/team.vue";
import Button from "@/components/partials/button.vue";
import Loading from "@/components/partials/loading.vue";
import Tooltip from "@/components/partials/templates/tooltip.vue";
import router from "@/router";
import { authApi } from "@/services/api";
import store from "@/store";
import toast from "@/toast.js";
import { SquaresPlusIcon } from "@heroicons/vue/24/outline";
import { PencilIcon } from "@heroicons/vue/24/solid";
import { ref } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
let openTeamModal = ref(false);
let loading = ref(true);
let teams = ref([]);
let teamId = ref("");

getTeams();

function getTeams() {
	loading.value = true;
	authApi
		.get(`teams/coach/${store.getters.getUser.id}`)
		.then(({ data }) => {
			teams.value = data;
			loading.value = false;
		})
		.catch(() => {
			toast.error(t("error.getTeamsApi"));
			loading.value = false;
		});
}
</script>
