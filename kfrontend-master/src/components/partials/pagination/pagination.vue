<template>
	<div class="inline-flex space-x-2 rounded-full">
		<PaginationItem
			v-if="props.current > 1"
			:text="'<<'"
			:active="false"
			@click="props.current > 1 && emit('pageChange', props.current - 1)" />
		<PaginationItem
			v-if="props.current > 6"
			:text="'1'"
			:active="false"
			@click="emit('pageChange', 1)" />
		<PaginationItem
			v-if="props.current > 7"
			:text="'...'"
			:clickable="false"
			:active="false"
			@click="null" />
		<PaginationItem
			v-for="index in props.pages"
			v-show="index >= pagesStart && index <= pagesEnd"
			:key="index"
			:text="index.toString()"
			:active="index === props.current"
			@click="props.current != index && emit('pageChange', index)" />
		<PaginationItem
			v-if="props.pages - props.current > 6"
			:text="'...'"
			:active="false"
			:clickable="false"
			@click="null" />
		<PaginationItem
			v-if="props.pages - props.current > 5"
			:text="props.pages.toString()"
			:active="false"
			@click="emit('pageChange', props.pages)" />
		<PaginationItem
			v-if="props.current < props.pages"
			:text="'>>'"
			:active="false"
			@click="props.current < props.pages && emit('pageChange', props.current + 1)" />
	</div>
</template>

<script setup>
import PaginationItem from "@/components/partials/pagination/paginationItem.vue";
import { ref, watch } from "vue";
const props = defineProps({
	pages: {
		type: Number,
		required: true,
	},
	current: {
		type: Number,
		required: true,
	},
});

const emit = defineEmits(["pageChange"]);
const pagesStart = ref(1);
const pagesEnd = ref(props.pages);

const reloadPagination = () => {
	pagesEnd.value = props.pages;
	pagesStart.value = 1;
	if (props.current > 5) pagesStart.value = props.current - 5;
	if (props.pages - props.current > 5) pagesEnd.value = props.current + 5;
};

watch(
	() => props.pages,
	() => {
		reloadPagination();
	},
	{ immediate: true }
);
watch(
	() => props.current,
	() => {
		reloadPagination();
	}
);
</script>
