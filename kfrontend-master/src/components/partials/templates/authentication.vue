<template>
	<div class="md:grid md:grid-cols-3 lg:grid-cols-2 xl:grid-cols-3">
		<div
			class="relative md:col-span-2 lg:col-span-1 min-h-screen flex flex-col justify-top px-6 lg:px-30 xl:px-45">
			<div
				class="max-w-2xl md:max-w-xl bg-white w-full left-0 absolute sm:relative md:top-1/2 md:-translate-y-1/2 mx-auto sm:pb-12 sm:rounded-2xl">
				<div class="sm:mx-auto sm:w-full sm:max-w-md pb-10 pt-12">
					<h2 class="mt-6 text-center text-5xl text-gray-900">
						{{ props.title }}
					</h2>
				</div>

				<slot></slot>
			</div>
		</div>
		<div class="md:col-span-1 xl:col-span-2 bg-primary-800">
			<div
				class="relative top-20 w-96 mx-auto cursor-pointer"
				@click="router.push({ name: 'Home' })">
				<Button :message="t('return')" :pill="true" type="primary" :submit="true" />
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import router from "@/router";

let { t } = useI18n();

const props = defineProps({
	title: {
		type: String,
		required: true,
	},
});
</script>

<i18n>
{
	"en_GB": {
		"return": "Return to the Home Page"
	},
	"pt_PT": {
		"return": "Voltar à página inicial"
	}
}
</i18n>
