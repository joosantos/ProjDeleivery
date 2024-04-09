<template>
	<div>
		<p v-if="matches.length" class="text-3xl font-medium capitalize text-center">
			{{ t("callHistory") }}
		</p>
		<div class="space-y-4 overflow-y-auto max-h-[600px]">
			<CallCard :matches="matches" @open-modal="null" />
		</div>
		<Button
			v-if="matches.length"
			class="capitalize mt-4 relative left-1/2 -translate-x-1/2 max-w-max"
			:message="t('deleteCallHistory')"
			:type="'primary'"
			:pill="true"
			@button-click="deleteHistory" />
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import CallCard from "@/components/competitionScreens/partials/callCard.vue";
import { ref, watch } from "vue";

let { t } = useI18n({ useScope: "global" });
const emit = defineEmits(["updated"]);
const props = defineProps({
	update: {
		type: Boolean,
		required: true,
	},
});
let matches = ref((JSON.parse(localStorage.getItem("callHistory")) || []).reverse());

watch(
	() => props.update,
	(after) => {
		if (after) {
			emit("updated");
			matches.value = JSON.parse(localStorage.getItem("callHistory")) || [];
			matches.value = matches.value.reverse();
			console.log(matches.value[0]);
		}
	}
);

function deleteHistory() {
	localStorage.setItem("callHistory", "[]");
	matches.value = [];
}
</script>
