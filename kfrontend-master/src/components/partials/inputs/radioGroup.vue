<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<label
			:class="[
				'block text-sm font-medium text-gray-700',
				props.capitalizeTitle && 'capitalize',
			]"
			>{{ label }}</label
		>
		<div class="relative mt-1 rounded-md">
			<fieldset class="mt-4">
				<legend class="sr-only">{{ label }}</legend>
				<div :class="`gap-y-4 grid grid-cols-${props.columns}`">
					<div
						v-for="option in props.radioOptions"
						:key="option.value"
						class="flex items-center ml-2">
						<input
							:id="option.value + '-' + (props.id == null ? props.name : props.id)"
							v-model="state"
							:name="props.id == null ? props.name : props.id"
							type="radio"
							:disabled="props.readonly"
							:value="option.value"
							:checked="state === option.value"
							class="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-500" />
						<label
							:for="option.value + '-' + (props.id == null ? props.name : props.id)"
							class="ml-3 block text-sm font-medium text-gray-700">
							{{ t(option.name) }}
						</label>
					</div>
				</div>
			</fieldset>
			<div
				v-if="error != ''"
				class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
				<ExclamationCircleIcon class="h-5 w-5 text-red-500" aria-hidden="true" />
			</div>
		</div>
		<p v-if="error != ''" class="mt-2 text-sm text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

const props = defineProps({
	// Name of the input for internal reference
	name: {
		type: String,
		required: true,
	},
	// ID of the input for internal reference
	id: {
		type: String,
		required: false,
		default: null,
	},
	// Label of the input to be displayed
	label: {
		type: String,
		required: true,
	},
	// Array of Objects
	// Objects syntax:
	// {
	//		name: "name",			text that will appear on radio label
	//		value: "value"			value emited when the option is clicked
	// }
	radioOptions: {
		type: Array,
		required: true,
	},
	// Value of the selected option if any
	optionSelected: {
		type: String,
		required: false,
		default: "",
	},
	// Error of the input field
	error: {
		type: String,
		required: true,
	},
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
	columns: {
		type: Number,
		required: false,
		default: 1,
	},
	capitalizeTitle: {
		type: Boolean,
		required: false,
		default: false,
	},
});

let state = ref(props.optionSelected);
const emit = defineEmits(["selected"]);

watch(
	() => state.value,
	(after) => {
		emit("selected", after);
	}
);

watch(
	() => props.optionSelected,
	(after) => {
		state.value = after;
	}
);
</script>
