<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<Combobox v-model="state" class="w-full" as="div">
			<label class="block text-sm text-left font-medium text-gray-700">
				{{ props.title }}
			</label>
			<div class="relative mt-1">
				<ComboboxInput
					:disabled="props.readonly"
					:class="[
						'w-full rounded-md border  bg-white py-2 pl-3 pr-10 shadow-sm focus:outline-none focus:ring-1 sm:text-sm',
						error == ''
							? 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
							: 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500',
					]"
					:display-value="
						() =>
							props.useTranslations
								? t(props.options.find((a) => a.id == state)?.name || '')
								: props.options.find((a) => a.id == state)?.name
					"
					@change="searchText = $event.target.value" />
				<ComboboxButton
					:disabled="props.readonly"
					class="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
					<ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
					<ExclamationCircleIcon
						v-if="error != ''"
						class="h-5 w-5 text-red-500"
						aria-hidden="true" />
				</ComboboxButton>

				<ComboboxOptions
					v-if="filteredOptions.length > 0"
					class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
					<ComboboxOption
						v-for="option in filteredOptions"
						:key="option.id"
						v-slot="{ active, selected }"
						:value="option"
						as="template">
						<li
							:class="[
								'relative cursor-default select-none py-2 pl-8 pr-4',
								active ? 'bg-indigo-600 text-white' : 'text-gray-900',
							]">
							<span
								:class="[
									'block truncate min-h-[1em]',
									selected && 'font-semibold',
								]">
								{{ props.useTranslations ? t(option.name) : option.name }}
							</span>

							<span
								v-if="option.id == state"
								:class="[
									'absolute inset-y-0 left-0 flex items-center pl-1.5',
									active ? 'text-white' : 'text-indigo-600',
								]">
								<CheckIcon class="h-5 w-5" aria-hidden="true" />
							</span>
						</li>
					</ComboboxOption>
				</ComboboxOptions>
			</div>
			<p
				v-if="error != ''"
				:id="props.id == null ? props.name : props.id"
				class="mt-2 text-sm text-red-600">
				{{ error }}
			</p>
		</Combobox>
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
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	// Array of Objects
	// Objects syntax:
	// {
	//		name: "name",		text that will appear on the select and will bbe searchable
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
	// Read Only Option
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
	useTranslations: {
		type: Boolean,
		required: false,
		default: false,
	},
});

let state = ref(props.optionSelected);

let searchText = ref("");
const emit = defineEmits(["selected"]);
let emitData = true;

watch(
	() => props.optionSelected,
	(after) => {
		emitData = false;
		state.value = after;
	}
);

watch(
	() => state.value,
	(after) => {
		if (emitData) {
			emit("selected", after.id);
		} else {
			emitData = true;
		}
	}
);
const filteredOptions = computed(() =>
	searchText.value === ""
		? props.options
		: props.options.filter((option) => {
				if (props.useTranslations)
					return t(option.name).toLowerCase().includes(searchText.value.toLowerCase());
				else return option.name.toLowerCase().includes(searchText.value.toLowerCase());
		  })
);
</script>
