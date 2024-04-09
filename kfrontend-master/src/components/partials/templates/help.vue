<template>
	<Tooltip :text="props.message">
		<QuestionMarkCircleIcon class="h-5 w-5 text-gray-400" />
	</Tooltip>
</template>
<script setup>
import Tooltip from "@/components/partials/templates/tooltip.vue";
import { QuestionMarkCircleIcon } from "@heroicons/vue/24/solid";
const props = defineProps({
	message: {
		type: String,
		required: true,
	},
});
</script>
