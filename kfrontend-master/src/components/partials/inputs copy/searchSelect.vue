<template>
	<div
		:class="[
			'custom-input-div',
			props.readonly && 'pointer-events-none opacity-25 select-none',
		]">
		<div :class="['custom-input-inner-div', error != '' ? 'bg-red-100' : '']">
			<Combobox v-model="state" as="div">
				<div class="relative">
					<ComboboxButton
						:class="[
							'absolute inset-0 z-10 w-full focus:outline-none',
							error == '' ? '' : 'right-1',
						]">
						<ChevronUpDownIcon
							class="h-5 w-5 text-gray-400 ml-auto mr-3"
							aria-hidden="true" />
					</ComboboxButton>

					<ComboboxInput
						:id="props.title"
						:readonly="props.readonly"
						:class="[
							'custom-input peer focus:text-black transition-all duration-200',
							state == '' ? 'text-transparent' : 'text-black',
						]"
						:display-value="
							(option) =>
								props.options.findIndex((a) => a.id == option) == -1
									? ''
									: props.options.find((a) => a.id == option)?.name
						"
						@change="filter($event.target.value)" />

					<label
						:for="props.title"
						:class="[
							'custom-input-label left-0 peer-focus:text-sm peer-focus:text-gray-800 peer-focus:top-2',
							state == ''
								? 'text-base text-gray-400 top-1/2 -translate-y-1/2'
								: 'text-sm text-gray-800',
						]">
						{{ props.title }}
					</label>

					<ComboboxOptions
						v-if="options.length > 0"
						class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 ring-1 ring-black ring-opacity-5 focus:outline-none">
						<ComboboxOption
							v-for="option in options"
							:key="option.id"
							v-slot="{ active, selected }"
							:value="option.id"
							as="template">
							<li
								:class="[
									'relative cursor-default select-none py-2 pl-3 pr-9',
									active ? 'bg-primary-500 text-white' : 'text-gray-900',
									selected ? 'bg-primary-200' : 'bg-none',
								]">
								<span>
									{{ option.name }}
								</span>

								<span
									v-if="selected"
									:class="[
										'absolute inset-y-0 right-0 flex items-center pr-4',
										active ? 'text-white' : 'text-primary-500',
									]">
									<CheckIcon class="h-5 w-5" aria-hidden="true" />
								</span>
							</li>
						</ComboboxOption>
					</ComboboxOptions>
					<div
						v-show="error != ''"
						class="absolute -right-2 top-1/2 -translate-y-1/2 pointer-events-none">
						<ExclamationCircleIcon class="h-5 w-5 text-red-700" aria-hidden="true" />
					</div>
				</div>
			</Combobox>
		</div>
		<p v-show="error != ''" class="mt-1 text-sm text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon, CheckIcon, ChevronUpDownIcon } from "@heroicons/vue/24/solid";
import {
	Combobox,
	ComboboxButton,
	ComboboxInput,
	ComboboxOption,
	ComboboxOptions,
} from "@headlessui/vue";
import { ref, watch } from "vue";

const props = defineProps({
	// Array of Objects
	// Objects syntax:
	// {
	//		name: "name",		text that will appear on the select
	//		id: "id"			value emited when the option is clicked
	// }
	options: {
		type: Array,
		required: true,
	},
	// Title of the selected
	title: {
		type: String,
		required: true,
	},
	// value of the selected option if any
	optionSelected: {
		type: String,
		required: false,
		default: "",
	},
	// Selected option if any
	error: {
		type: String,
		required: true,
	},
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
});

let state = ref(props.optionSelected);

let options = ref(props.options);
const emit = defineEmits(["selected"]);

watch(
	() => state.value,
	(after) => {
		emit("selected", after);
	}
);

function filter(searchText) {
	if (searchText == "") {
		options.value = props.options;
		state.value = "";
	}
	options.value = props.options.filter((a) =>
		a.name.toLowerCase().includes(searchText.toLowerCase())
	);
}
</script>
