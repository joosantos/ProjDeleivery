<template>
	<form
		:class="[
			'grid grid-cols-1 w-full px-4 py-2 bg-gray-100 border border-gray-300 space-y-2 rounded-lg justify-center relative left-1/2 -translate-x-1/2',
			props.disabled && 'opacity-50 pointer-events-none',
		]"
		@submit.prevent="emit('submitForm')">
		<slot></slot>
		<div class="inline-flex space-x-4 mx-auto">
			<Trash :text="t(props.trashText)" @button-click="emit('clearForm')" />
			<Button
				class="max-w-max px-4"
				:message="t(props.buttonText)"
				:type="'primary'"
				:pill="true"
				:size="'small'"
				:submit="true"
				:loading="props.loading"
				:show-check="props.showCheck"
				:show-x="props.showX"
				:up-on-hover="false"
				@button-click="null" />
		</div>
	</form>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import Trash from "@/components/partials/inputs/trash.vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

const emit = defineEmits(["submitForm", "clearForm"]);
const props = defineProps({
	buttonText: {
		type: String,
		required: false,
		default: "forms.search",
	},
	buttonLoading: {
		type: Boolean,
		required: false,
		default: false,
	},
	trashText: {
		type: String,
		required: false,
		default: "forms.clearForm",
	},
	loading: {
		type: Boolean,
		required: false,
		default: false,
	},
	showCheck: {
		type: Boolean,
		required: false,
		default: false,
	},
	disabled: {
		type: Boolean,
		required: false,
		default: false,
	},
	showX: {
		type: Boolean,
		required: false,
		default: false,
	},
});
</script>
