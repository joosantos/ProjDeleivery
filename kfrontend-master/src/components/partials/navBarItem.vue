<template>
	<router-link
		:class="[
			'font-medium rounded-full border-2 py-2 px-6 min-w-max',
			props.current
				? 'font-bold text-black border-blue-600 '
				: 'cursor-pointer border-blue-400  hover:bg-blue-400 text-gray-500 hover:text-black active:ring-2 ring-offset-2 ring-blue-500 active:border-blue-300 ring-offset-blue-300',
		]"
		:to="{ name: props.route }">
		<div class="inline-flex md:min-w-[6rem] mt-1">
			<component
				:is="
					props.outline == null ? props.icon : props.current ? props.icon : props.outline
				"
				v-if="props.icon != null"
				class="mr-1 ml-auto flex-shrink-0 h-6 w-6"
				aria-hidden="true" />
			<p class="ml-0 mr-auto">
				{{ t(props.name) }}
			</p>
		</div>
	</router-link>
</template>

<script setup>
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });
const props = defineProps({
	current: {
		type: Boolean,
		required: false,
		default: false,
	},
	route: {
		type: String,
		required: true,
	},
	name: {
		type: String,
		required: false,
		default: "",
	},
	icon: {
		type: Function,
		required: false,
		default: null,
	},
	outline: {
		type: Function,
		required: false,
		default: null,
	},
});
</script>
