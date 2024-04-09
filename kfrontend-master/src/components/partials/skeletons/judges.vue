<template>
	<div class="flex flex-col">
		<div class="flex justify-between">
			<p class="w-full text-center">{{ props.judge1 }}</p>
			<p class="w-full text-center">{{ props.central }}</p>
			<p class="w-full text-center">{{ props.judge2 }}</p>
		</div>
		<div class="flex justify-between">
			<div class="w-full px-6">
				<hr class="w-full border-black border bottom-full" />
			</div>
			<div class="w-full px-6">
				<hr class="w-full border-black border bottom-full" />
			</div>
			<div class="w-full px-6">
				<hr class="w-full border-black border bottom-full" />
			</div>
		</div>
		<div class="flex justify-between">
			<p class="w-full text-center">{{ t("judge1") }}</p>
			<p class="w-full text-center">{{ t("central") }}</p>
			<p class="w-full text-center">{{ t("judge2") }}</p>
		</div>
	</div>
</template>

<script setup>
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	judge1: {
		type: String,
		required: false,
		default: "",
	},
	judge2: {
		type: String,
		required: false,
		default: "",
	},
	central: {
		type: String,
		required: false,
		default: "",
	},
	absolute: {
		type: Boolean,
		required: false,
		default: false,
	},
});
</script>

<i18n>
{
  "en_GB": {
	  "judge1": "Judge 1",
	  "judge2": "Judge 2",
	  "central": "Central Referee"
  },
  "pt_PT": {
	  "judge1": "Juíz 1",
	  "judge2": "Juíz 2",
	  "central": "Árbitro Central"
  }
}
</i18n>
