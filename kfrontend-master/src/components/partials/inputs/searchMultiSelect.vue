<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<label class="block text-sm font-medium text-gray-700">
			{{ props.title }}
		</label>

		<Multiselect
			v-model="state"
			:label="props.name"
			:props.placeholder="props.label || 'all'"
			:disabled="props.readonly"
			:searchable="true"
			:class="['mt-1', !!props.error && 'border-red-500']"
			@open="focusSearch"
			@clear="emit('selected', state)"
			@select="emit('selected', state)"
			@deselect="emit('selected', state)"
			mode="tags"
			:options="
				props.options.map((a) => ({
					value: a.id,
					label: props.useTranslations ? t(a.name) : a.name,
				}))
			">
			<template #option="{ option }">
				{{ option.label }}
			</template>

			<template #caret="{ handleCaretClick, isOpen }">
				<span :class="['mr-2.5 inline-flex', !isOpen && 'pointer-events-none']">
					<ExclamationCircleIcon
						v-if="!!props.error"
						class="h-5 w-5 text-red-500"
						aria-hidden="true" />
					<ChevronUpDownIcon
						class="h-5 w-5"
						aria-hidden="true"
						@click="handleCaretClick" />
				</span>
			</template>

			<template #noresults>
				<span class="multiselect-no-results"> {{ t("error.noResults") }}</span>
			</template>
		</Multiselect>
		<p
			v-if="error != ''"
			:id="props.id == null ? props.name : props.id"
			class="mt-2 text-sm text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon, ChevronUpDownIcon } from "@heroicons/vue/24/solid";
import Multiselect from "@vueform/multiselect";
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	// [{id: "value to return in list", name: "name to be displayed"}]
	options: {
		type: Array,
		required: true,
	},
	title: {
		type: String,
		required: true,
	},
	label: {
		type: String,
		required: false,
		default: "",
	},
	optionSelected: {
		type: Array,
		required: false,
		default: [],
	},
	error: {
		type: String,
		required: false,
		default: "",
	},
	placeholder: {
		type: String,
		required: false,
	},
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

const state = ref(props.optionSelected);

const emit = defineEmits(["selected"]);
const focusSearch = (select) => {
	setTimeout(() => select.$el.getElementsByClassName("multiselect-tags-search")[0].focus(), 100);
};
watch(
	() => props.optionSelected,
	(after) => {
		state.value = after;
	}
);
</script>

<style src="@vueform/multiselect/themes/default.css"></style>
<style>
.multiselect {
	border-radius: 0.375rem;
}
.multiselect.is-active {
	box-shadow: 0 0 0 2px rgba(99, 102, 241, 1);
}

.multiselect-tags-search {
	--tw-ring-color: #fff !important;
	padding: 0 !important;
}

.multiselect-tags-search-wrapper {
	display: none;
}

.is-active .multiselect-tags-search-wrapper,
.is-open .multiselect-tags-search-wrapper {
	display: block;
	margin: 0;
	display: block;
	flex-grow: 0;
	flex-shrink: 0;
	height: 100%;
	width: 100%;
	position: relative;
}
</style>
