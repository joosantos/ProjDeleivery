<template>
	<div :class="['flex items-center border-0', props.readonly && 'opacity-50']">
		<Switch
			v-model="enabled"
			:disabled="props.readonly"
			:class="[
				enabled ? 'bg-indigo-600' : 'bg-gray-200',
				'relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500',
			]"
			@click="emit('valueChanged', !enabled)">
			<span
				aria-hidden="true"
				:class="[
					enabled ? 'translate-x-5' : 'translate-x-0',
					'pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200',
				]" />
		</Switch>
		<label
			class="ml-3 select-none"
			@click="
				enabled = !enabled;
				emit('valueChanged', enabled);
			">
			<span class="text-sm font-medium text-gray-900">{{ props.label }}</span>
			<span class="text-sm text-gray-500">{{ props.subLabel }}</span>
		</label>
	</div>
</template>

<script setup>
import { ref, watch } from "vue";
import { Switch } from "@headlessui/vue";

const props = defineProps({
	label: {
		type: String,
		required: true,
	},
	subLabel: {
		type: String,
		required: false,
		default: "",
	},
	optionSelected: {
		type: Boolean,
		required: false,
		default: false,
	},
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
});
const emit = defineEmits(["valueChanged"]);

let enabled = ref(props.optionSelected);

watch(
	() => props.optionSelected,
	(after) => {
		enabled.value = after;
	}
);
</script>
