<template>
	<Modal :open="props.open" :outside-click="true" :show-x="true" @close="emit('close')">
		<Loading v-if="loading" :size="10" />
		<div v-else class="-mt-8">
			<p class="text-2xl font-medium">
				{{ t("selectTeam") }}
			</p>
			<SearchSelect
				:title="t('team')"
				:option-selected="teamSelected"
				:options="teams"
				:error="t(teamError)"
				@selected="
					(option) => {
						teamSelected = option;
					}
				" />
			<div class="space-x-16 mt-4 mx-auto max-w-max">
				<Button
					class="max-w-max px-8"
					:message="t('cancel')"
					:type="'primary'"
					:pill="true"
					@button-click="emit('close')" />
				<Button
					class="max-w-max px-8"
					:message="t('select')"
					:type="'success'"
					:pill="true"
					@button-click="emitTeam" />
			</div>
		</div>
	</Modal>
</template>

<script setup>
import Modal from "@/components/partials/modal.vue";
import Loading from "@/components/partials/loading.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Button from "@/components/partials/button.vue";
import { ref, onMounted, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["close", "selected"]);

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
});

const teams = ref([]);
const teamSelected = ref("");
const loading = ref(true);
const teamError = ref("");

const getTeams = async () => {
	loading.value = true;
	try {
		const { data } = await authApi.get("teams");
		teams.value = data.map((team) => ({
			id: team.id,
			name: `${team.name} (${team.abbreviation})`,
		}));
	} catch (e) {
		errorHandling(e);
	} finally {
		loading.value = false;
	}
};

onMounted(async () => {
	getTeams();
});

watch(
	() => teamSelected.value,
	() => {
		teamError.value = "";
	}
);

watch(
	() => props.open,
	() => {
		teamSelected.value = "";
		teamError.value = "";
	}
);

const emitTeam = () => {
	if (!teamSelected.value) {
		teamError.value = "error.required";
		return;
	}
	emit("close");
	emit("selected", teamSelected.value, teams.value.find((a) => a.id == teamSelected.value).name);
};
</script>
