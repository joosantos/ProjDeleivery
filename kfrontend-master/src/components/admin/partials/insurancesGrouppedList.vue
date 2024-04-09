<template>
	<div
		class="grid 2xl:grid-cols-6 lg:grid-cols-4 sm:grid-cols-2 grid-cols-1 justify-center gap-y-4 gap-x-4 mt-4">
		<router-link
			v-for="insurance of insurances"
			:key="insurance.id"
			:to="{
				name: 'Insurances Group Details',
				query: {
					paymentcomprovativeurl:
						props.grouppedBy === 'payment_comprovatives'
							? insurance?.payment_comprovative_url || 'none'
							: '',
					insurancegroup:
						props.grouppedBy === 'insurance_groups'
							? insurance?.insurance_group_id || 'without'
							: '',
				},
			}"
			class="mx-auto cursor-pointer border rounded-lg px-4 py-2 w-full relative bg-blue-100 border-blue-300 hover:bg-blue-200">
			<p
				v-if="props.grouppedBy === 'insurance_groups'"
				class="text-xl font-semibold text-center line-clamp-1">
				{{ insurance.insurance_group_name || t("withoutGroup") }}
			</p>
			<div v-else>
				<p
					v-if="insurance.teams.length === 1"
					class="text-xl font-semibold text-center line-clamp-1">
					{{ insurance.teams[0].abbreviation }}
				</p>
				<p v-else class="text-xl font-semibold text-center line-clamp-1">
					{{
						insurance.teams
							.map((a) => a.abbreviation)
							.sort()
							.join(", ")
					}}
				</p>
			</div>
			<div v-if="props.grouppedBy === 'payment_comprovatives'" class="w-full">
				<button
					class="link text-lg mt-2"
					@click.prevent="getPaymentGuide(insurance.payment_comprovative_url)">
					{{ t("getPaymentGuide") }}
				</button>
				<br />
				<a
					v-if="insurance.payment_comprovative_url"
					class="link text-lg"
					target="_blank"
					:href="
						'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
						insurance.payment_comprovative_url
					">
					{{ t("paymentComprovative") }}
				</a>
				<p v-else class="text-lg">
					{{ t("noPaymentComprovative") }}
				</p>
			</div>

			<!-- Medical Exams -->
			<div class="w-full mt-4">
				<p>{{ t("medicalExams") }}</p>
				<LoadingBar
					:size="'small'"
					:progress="(insurance.number_medical_exams * 100) / insurance.number_insured"
					:variant="
						insurance.number_medical_exams === insurance.number_insured
							? 'success'
							: 'warning'
					" />
				<p class="text-center w-full">
					{{
						t("numberOfNumber", {
							number1: insurance.number_medical_exams,
							number2: insurance.number_insured,
						})
					}}
				</p>
			</div>

			<!-- Payment Comprovatives -->
			<div v-if="props.grouppedBy !== 'payment_comprovatives'" class="w-full">
				<p>
					{{ t("missingPaymentComprovative") }}
				</p>
				<LoadingBar
					:size="'small'"
					:progress="
						(insurance.number_payment_comprovatives * 100) / insurance.number_insured
					"
					:variant="
						insurance.number_payment_comprovatives === insurance.number_insured
							? 'success'
							: 'warning'
					" />
				<p class="text-center w-full">
					{{
						t("numberOfNumber", {
							number1: insurance.number_payment_comprovatives,
							number2: insurance.number_insured,
						})
					}}
				</p>
			</div>

			<!-- Requestss Status -->
			<div class="w-full">
				<p>{{ t("requestsStatus") }}</p>
				<div class="grid grid-cols-1 w-full">
					<div class="inline-flex">
						<div class="w-4 mt-1 h-4 rounded-full bg-red-500"></div>
						<p class="ml-2">
							{{ t("federationRequest.other", insurance.number_other_status) }}
						</p>
					</div>
					<div class="inline-flex">
						<div class="w-4 mt-1 h-4 rounded-full bg-blue-500"></div>
						<p class="ml-2">
							{{ t("federationRequest.pending", insurance.number_pending) }}
						</p>
					</div>
					<div class="inline-flex">
						<div class="w-4 mt-1 h-4 rounded-full bg-green-500"></div>
						<p class="ml-2">
							{{ t("federationRequest.accepted", insurance.number_accepted) }}
						</p>
					</div>
				</div>
				<MultipleLoadingBar
					:size="'small'"
					:bars="[
						{
							progress:
								(insurance.number_other_status * 100) / insurance.number_insured,
							variant: 'danger',
						},
						{
							progress: (insurance.number_pending * 100) / insurance.number_insured,
							variant: 'primary',
						},
						{
							progress: (insurance.number_accepted * 100) / insurance.number_insured,
							variant: 'success',
						},
					]"
					:variant="'success'" />
			</div>

			<!-- Images -->
			<div class="w-full inline-flex relative h-10">
				<img
					class="rounded-full w-10 h-10 absolute border border-gray-600"
					:style="`left: ${idx * 24}px`"
					v-for="(url, idx) in insurance.profile_pictures"
					v-show="idx < 10"
					:key="url"
					:src="
						url && url.split('/').at(-1) != 'None'
							? `https://kempo-files.fra1.digitaloceanspaces.com/${url}`
							: '/defaultUserImage.png'
					"
					alt="Image" />
			</div>
		</router-link>
	</div>
</template>

<script setup>
import { useI18n } from "vue-i18n";
import LoadingBar from "@/components/partials/loadingBar.vue";
import MultipleLoadingBar from "@/components/partials/multipleLoadingBar.vue";
import { PencilIcon, ArrowLeftIcon, PlusIcon } from "@heroicons/vue/24/solid";
import { authApi, errorHandling } from "@/services/api";

let { t } = useI18n({ useScope: "global" });
const props = defineProps({
	insurances: {
		type: Array,
		required: true,
	},
	grouppedBy: {
		type: String,
		required: true,
	},
});

const getPaymentGuide = async (payment_comprovative_url) => {
	try {
		const { data } = await authApi.get(
			`insurances/get-payment-guide?payment_comprovative=${payment_comprovative_url}`,
			{ responseType: "blob" }
		);

		const pdfUrl = URL.createObjectURL(data);
		const a = document.createElement("a");
		a.download = "payment_guide.pdf";
		a.href = pdfUrl;
		a.target = "_self";
		a.click();

		setTimeout(function () {
			// For Firefox it is necessary to delay revoking the ObjectURL
			a.remove();
			URL.revokeObjectURL(pdfUrl);
		}, 100);
	} catch (e) {
		console.error(e);
		errorHandling(e);
	}
};
</script>
