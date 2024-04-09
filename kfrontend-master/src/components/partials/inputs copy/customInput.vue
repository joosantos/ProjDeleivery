<template>
	<div class="custom-input-div">
		<div
			:class="[
				'custom-input-inner-div',
				error != '' ? 'bg-red-100' : '',
				props.readonly && 'opacity-25 pointer-events-none select-none',
			]">
			<input
				v-if="props.mask == ''"
				:id="props.name"
				v-model="state"
				:type="props.type"
				:name="props.name"
				placeholder=""
				class="custom-input peer"
				:readonly="props.readonly" />
			<input
				v-else
				:id="props.name"
				v-model="state"
				v-mask="props.mask"
				:type="props.type"
				:name="props.name"
				placeholder=""
				class="custom-input peer"
				:readonly="props.readonly" />
			<label
				:for="props.name"
				:class="[
					'custom-input-label',
					!props.readonly &&
						'peer-focus:text-sm peer-focus:text-gray-800 peer-focus:top-2 peer-focus:-translate-y-0',
					state == ''
						? 'text-base text-gray-400 top-1/2 -translate-y-1/2'
						: 'top-2 -translate-y-0',
				]">
				{{ props.label }}
			</label>
			<div
				v-show="error != ''"
				class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
				<ExclamationCircleIcon class="h-5 w-5 text-red-700" aria-hidden="true" />
			</div>
		</div>
		<p v-show="error != ''" class="order-last mt-1 text-sm text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";

const props = defineProps({
	// Type of the input
	type: {
		type: String,
		required: true,
		validator(value) {
			// The type must match one of these strings
			return ["text", "password"].includes(value);
		},
	},
	// Name of the input for internal reference
	name: {
		type: String,
		required: true,
	},
	// Label of the input to be displayed
	label: {
		type: String,
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
	mask: {
		type: String,
		required: false,
		default: "",
	},
});

let state = ref(props.optionSelected);
const emit = defineEmits(["valueChanged"]);

watch(
	() => props.optionSelected,
	(after) => {
		state.value = after;
	}
);

watch(
	() => state.value,
	(after) => {
		emit("valueChanged", after);
	}
);
</script>
