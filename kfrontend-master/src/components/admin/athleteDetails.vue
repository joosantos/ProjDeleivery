<template>
	<div>
		<Loading v-if="loading || initialLoading" :size="10" />
		<div v-else class="lg:grid lg:grid-cols-12 lg:gap-x-5 scroll-smooth">
			<!-- Nav Bar -->
			<aside class="py-6 px-2 md:px-6 lg:col-span-3 lg:py-0 lg:px-0">
				<nav class="sticky top-44 space-y-1">
					<a
						v-for="item in navigation"
						:id="item.id"
						:key="item.name"
						:href="item.href"
						:class="[
							item.current
								? 'bg-gray-50 text-indigo-700 hover:text-indigo-700 hover:bg-white'
								: 'text-gray-900 hover:text-gray-900 hover:bg-gray-50',
							'group rounded-md px-3 py-2 flex items-center text-md font-medium',
						]"
						:aria-current="item.current ? 'page' : undefined">
						<component
							:is="item.icon"
							:class="[
								item.current
									? 'text-indigo-500 group-hover:text-indigo-500'
									: 'text-gray-400 group-hover:text-gray-500',
								'flex-shrink-0 -ml-1 mr-3 h-6 w-6',
							]"
							aria-hidden="true" />
						<span class="truncate">{{ item.name }}</span>
					</a>
				</nav>
			</aside>

			<div v-if="loadingForm" class="col-span-full">
				<Loading :size="10" />
			</div>
			<!-- Form -->
			<div v-else class="space-y-6 md:px-6 lg:col-span-9 lg:px-0">
				<!-- Public Information Form -->
				<FormAthlete
					id="publicInformationForm"
					:title="t('label.information.public.title')"
					:subtitle="t('label.information.public.sub')"
					:button-save="t('saveButton')"
					:button-edit="t('editButton')"
					:show-button="isEdit"
					:can-edit="canEdit.public"
					@submited="isEdit ? editAthlete('public') : createAthlete()"
					@edit="canEdit.public = true">
					<!-- Image Input -->
					<div class="col-span-12 md:col-span-4 md:col-start-6 md:row-span-5">
						<ImageInput
							:name="'profilePicture'"
							:label="t('form.profilePicture')"
							:error="''"
							:original-image="imageUrl"
							:url-default-image="'/defaultUserImage.png'"
							:readonly="!canEdit.public"
							@value-changed="saveProfilePictureToSaveLater" />
					</div>
					<!-- Name Input -->
					<div class="col-span-12 md:col-span-5 md:row-start-1 md:col-start-1">
						<CustomInput
							:type="'text'"
							:name="'name'"
							:label="t('form.name')"
							:option-selected="state.name"
							:error="v$.name.$errors.length == 0 ? '' : v$.name.$errors[0].$message"
							:readonly="!canEdit.public"
							@value-changed="(option) => (state.name = option)" />
					</div>
					<!-- Team Input -->
					<div class="col-span-12 md:col-span-5 md:row-start-2 md:col-start-1">
						<SearchSelect
							:options="teams"
							:title="t('form.team')"
							:option-selected="state.team"
							:readonly="!canEdit.public || !canEdit.team"
							:error="''"
							@selected="(option) => (state.team = option)" />
					</div>
					<!-- Belt Input -->
					<div class="col-span-12 md:col-span-5 md:row-start-3 md:col-start-1">
						<SearchSelect
							:options="belts"
							:title="t('form.belt')"
							:option-selected="state.belt"
							:readonly="!canEdit.public"
							:useTranslations="true"
							:error="
								store.getters.getUserRole == 'ADMIN' || v$.belt.$errors.length == 0
									? ''
									: v$.belt.$errors[0].$message
							"
							@selected="(option) => (state.belt = option)" />
					</div>
					<!-- Weight Input -->
					<div class="col-span-12 md:col-span-5 md:row-start-4 md:col-start-1">
						<CustomInput
							type="text"
							:label="t('form.weight')"
							:name="'weight'"
							:readonly="!canEdit.public"
							:option-selected="state.weight.toString()"
							:error="
								store.getters.getUserRole == 'ADMIN' ||
								v$.weight.$errors.length == 0
									? ''
									: v$.weight.$errors[0].$message
							"
							@value-changed="
								(option) => (state.weight = option.replace(',', '.'))
							" />
					</div>
					<!-- Birthday Input -->
					<div class="col-span-12 md:col-span-5 md:row-start-5 md:col-start-1">
						<DateInput
							:label="t('form.birthday')"
							:readonly="!canEdit.public"
							:name="'birthday'"
							:option-selected="state.birthday"
							:error="
								store.getters.getUserRole == 'ADMIN' ||
								v$.birthday.$errors.length == 0
									? ''
									: v$.birthday.$errors[0].$message
							"
							@value-changed="(option) => (state.birthday = option)" />
					</div>
					<!-- Is Adapted Input -->
					<div class="col-span-12 md:col-span-3 md:col-start-1">
						<ToogleInput
							:label="t('form.isAdapted')"
							:name="'isAdapted'"
							:readonly="!canEdit.public"
							:option-selected="state.isAdapted"
							:error="
								v$.isAdapted.$errors.length == 0
									? ''
									: v$.isAdapted.$errors[0].$message
							"
							@value-changed="(option) => (state.isAdapted = option)" />
					</div>
					<!-- Gender Input -->
					<div class="col-span-6 md:col-span-3">
						<RadioGroup
							:label="t('form.genderIsMale')"
							:name="'genderIsMale'"
							:readonly="!canEdit.public"
							:option-selected="state.genderIsMale"
							:radio-options="[
								{ name: 'masc', value: 'M' },
								{ name: 'fem', value: 'F' },
								{
									name: 'other',
									value: 'O',
								},
							]"
							:error="
								store.getters.getUserRole == 'ADMIN' ||
								v$.genderIsMale.$errors.length == 0
									? ''
									: v$.genderIsMale.$errors[0].$message
							"
							@selected="(option) => (state.genderIsMale = option)" />
					</div>
					<!-- Competition Gender Input -->
					<div v-if="state.genderIsMale == 'O'" class="col-span-6 md:col-span-4">
						<RadioGroup
							:label="t('form.isMale')"
							:name="'isMale'"
							:readonly="!canEdit.public"
							:option-selected="state.isMale"
							:radio-options="[
								{ name: 'masc', value: 'M' },
								{ name: 'fem', value: 'F' },
							]"
							:error="
								store.getters.getUserRole == 'ADMIN' ||
								v$.isMale.$errors.length == 0
									? ''
									: v$.isMale.$errors[0].$message
							"
							@selected="(option) => (state.isMale = option)" />
					</div>
				</FormAthlete>

				<!-- Private Information Form -->
				<FormAthlete
					id="privateInformationForm"
					:title="t('label.information.private.title')"
					:subtitle="t('label.information.private.sub')"
					:button-save="t('saveButton')"
					:button-edit="t('editButton')"
					:can-edit="canEdit.private"
					@submited="isEdit ? editAthlete('private') : createAthlete()"
					@edit="canEdit.private = true">
					<!-- Federation Active Input -->
					<div class="col-span-12 md:col-span-4">
						<ToogleInput
							:type="'text'"
							:name="'federationActive'"
							:label="t('form.federationActive')"
							:option-selected="state.federationActive"
							:error="''"
							:readonly="!canEdit.private || store.getters.getUserRole != 'ADMIN'"
							@value-changed="(option) => (state.federationActive = option)" />
					</div>
					<!-- Federation Number Input -->
					<div class="col-span-12 md:col-span-4 md:col-start-6">
						<CustomInput
							:type="'text'"
							:name="'federationNumber'"
							:label="t('form.federationNumber')"
							:option-selected="(state.federationNumber || '').toString()"
							:error="''"
							:readonly="!canEdit.private || store.getters.getUserRole != 'ADMIN'"
							@value-changed="(option) => (state.federationNumber = option)" />
					</div>
					<!-- Email Input -->
					<div class="col-span-12 md:col-span-4">
						<CustomInput
							:type="'text'"
							:name="'email'"
							:label="t('form.email')"
							:option-selected="state.email"
							:error="''"
							:readonly="!canEdit.private"
							@value-changed="(option) => (state.email = option)" />
					</div>
					<!-- Phone Input -->
					<div class="col-span-12 md:col-span-4 md:col-start-6">
						<CustomInput
							:type="'text'"
							:name="'phone'"
							:label="t('form.phone')"
							:option-selected="state.phone"
							:error="''"
							:readonly="!canEdit.private"
							@value-changed="(option) => (state.phone = option)" />
					</div>
					<!-- Nationality Input -->
					<div class="col-span-12 md:col-span-3 md:col-start-1">
						<SearchSelect
							:title="t('form.nationality')"
							:options="countries"
							:option-selected="state.nationality"
							:readonly="!canEdit.private"
							:error="''"
							@selected="(option) => (state.nationality = option)" />
					</div>
					<!-- Naturality Region Input -->
					<div class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('form.naturalityRegion')"
							:name="'naturalRegion'"
							:readonly="!canEdit.private"
							:option-selected="state.naturalRegion"
							:error="''"
							@value-changed="(option) => (state.naturalRegion = option)" />
					</div>
					<!-- Naturality Country Input -->
					<div class="col-span-12 md:col-span-3">
						<!-- Naturality Country Input -->
						<SearchSelect
							:title="t('form.naturalityCountry')"
							:options="countries"
							:option-selected="state.naturalCountry"
							:readonly="!canEdit.private"
							:error="''"
							@selected="(option) => (state.naturalCountry = option)" />
					</div>

					<!-- Identification Document Type Input -->
					<div class="col-span-12 md:col-span-4 col-start-1">
						<RadioGroup
							:label="t('identificationDocument.type')"
							:name="'identificationDocumentType'"
							:readonly="!canEdit.private"
							:option-selected="state.identificationDocumentType"
							:columns="2"
							:radio-options="[
								{
									name: 'identificationDocument.cc',
									value: 'C',
								},
								{
									name: 'identificationDocument.bi',
									value: 'I',
								},
								{
									name: 'identificationDocument.birthBulletin',
									value: 'B',
								},
								{
									name: 'identificationDocument.passport',
									value: 'P',
								},
								{
									name: 'other',
									value: 'O',
								},
							]"
							:error="''"
							@selected="(option) => (state.identificationDocumentType = option)" />
					</div>
					<!-- Identification Document Other Type Input -->
					<div
						v-if="state.identificationDocumentType == 'O'"
						class="col-span-12 md:col-span-4 md:col-start-6">
						<CustomInput
							type="text"
							:label="t('identificationDocument.otherType')"
							:name="'otherIdentificationDocumentType'"
							:readonly="!canEdit.private"
							:option-selected="state.otherIdentificationDocumentType"
							:error="''"
							@value-changed="
								(option) => (state.otherIdentificationDocumentType = option)
							" />
					</div>
					<!-- Identification Document Number Input -->
					<div class="col-span-12 md:col-span-3 md:col-start-1">
						<CustomInput
							type="text"
							:label="t('identificationDocument.number')"
							:name="'identificationDocumentNumber'"
							:readonly="!canEdit.private"
							:option-selected="state.identificationDocumentNumber"
							:error="''"
							@value-changed="
								(option) => (state.identificationDocumentNumber = option)
							" />
					</div>
					<!-- Identification Document Emitted By Input -->
					<div
						v-if="state.identificationDocumentType != 'C'"
						class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('identificationDocument.emitedBy')"
							:name="'identificationDocumentEmittedBy'"
							:readonly="!canEdit.private"
							:option-selected="state.identificationDocumentEmittedBy"
							:error="''"
							@value-changed="
								(option) => (state.identificationDocumentEmittedBy = option)
							" />
					</div>
					<!-- Identification Document Expiration Date Input -->
					<div class="col-span-12 md:col-span-3">
						<DateInput
							:label="t('identificationDocument.expirationDate')"
							:readonly="!canEdit.private"
							:name="'identificationDocumentExpirationDate'"
							:option-selected="state.identificationDocumentExpirationDate"
							:error="''"
							@value-changed="
								(option) => (state.identificationDocumentExpirationDate = option)
							" />
					</div>
					<!-- NIF Input -->
					<div class="col-span-12 md:col-span-4">
						<CustomInput
							type="text"
							:label="t('form.nif')"
							:name="'nif'"
							:readonly="!canEdit.private"
							:option-selected="state.nif"
							:error="''"
							@value-changed="(option) => (state.nif = option)" />
					</div>

					<!-- Address Title -->
					<div class="md:border-t md:border-gray-200 md:pt-5 col-span-12">
						<h3 class="text-lg font-medium leading-6 text-gray-900">
							{{ t("title.address") }}
						</h3>
					</div>
					<!-- Address Input -->
					<div class="col-span-12 md:col-span-9">
						<TextAreaInput
							:rows="3"
							:label="t('form.address')"
							:name="'address'"
							:readonly="!canEdit.private"
							:option-selected="state.address"
							:error="''"
							@value-changed="(option) => (state.address = option)" />
					</div>
					<!-- City Input -->
					<div class="col-span-12 md:col-span-3 md:col-start-1">
						<CustomInput
							type="text"
							:label="t('form.city')"
							:name="'city'"
							:readonly="!canEdit.private"
							:option-selected="state.city"
							:error="''"
							@value-changed="(option) => (state.city = option)" />
					</div>
					<!-- Zip Code Input -->
					<div class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('form.zipCode')"
							:name="'zipCode'"
							:mask="'####-###'"
							:readonly="!canEdit.private"
							:option-selected="state.zipCode"
							:error="''"
							@value-changed="(option) => (state.zipCode = option)" />
					</div>
					<!-- District Input -->
					<div class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('form.district')"
							:name="'district'"
							:readonly="!canEdit.private"
							:option-selected="state.district"
							:error="''"
							@value-changed="(option) => (state.district = option)" />
					</div>
					<!-- Region Input -->
					<div class="col-span-12 md:col-span-4 md:col-start-1">
						<SearchSelect
							:options="regions"
							:title="t('form.region')"
							:option-selected="state.region"
							:readonly="!canEdit.private"
							:error="''"
							@selected="(option) => (state.region = option)" />
					</div>
					<!-- Country Input -->
					<div class="col-span-12 md:col-span-4 md:col-start-6">
						<SearchSelect
							:title="t('form.country')"
							:options="countries"
							:option-selected="state.country"
							:readonly="!canEdit.private"
							:error="''"
							@selected="(option) => (state.country = option)" />
					</div>

					<!-- Athlete's Responsible Title -->
					<div
						v-if="showResponsible"
						class="md:border-t md:border-gray-200 md:pt-5 col-span-12">
						<h3 class="text-lg font-medium leading-6 text-gray-900">
							{{ t("title.responsible") }}
						</h3>
					</div>
					<!-- Athlete's Responsible Name Input -->
					<div v-if="showResponsible" class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('form.responsible.name')"
							:name="'responsibleName'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleName"
							:error="''"
							@value-changed="(option) => (state.responsibleName = option)" />
					</div>
					<!-- Athlete's Responsible Email Input -->
					<div v-if="showResponsible" class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('form.responsible.email')"
							:name="'responsibleEmail'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleEmail"
							:error="''"
							@value-changed="(option) => (state.responsibleEmail = option)" />
					</div>
					<!-- Athlete's Responsible Relationship Input -->
					<div v-if="showResponsible" class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('form.responsible.relationship')"
							:name="'responsibleRelationship'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleRelationship"
							:error="''"
							@value-changed="(option) => (state.responsibleRelationship = option)" />
					</div>

					<!-- Athlete's Responsible Identification Document Type Input -->
					<div v-if="showResponsible" class="col-span-12 md:col-span-4 col-start-1">
						<RadioGroup
							:label="t('identificationDocument.type')"
							:name="'responsibleIdentificationDocumentType'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleIdentificationDocumentType"
							:columns="2"
							:radio-options="[
								{
									name: 'identificationDocument.cc',
									value: 'C',
								},
								{
									name: 'identificationDocument.bi',
									value: 'I',
								},
								{
									name: 'identificationDocument.birthBulletin',
									value: 'B',
								},
								{
									name: 'identificationDocument.passport',
									value: 'P',
								},
								{
									name: 'other',
									value: 'O',
								},
							]"
							:error="''"
							@selected="
								(option) => (state.responsibleIdentificationDocumentType = option)
							" />
					</div>
					<!-- Athlete's Responsible Identification Document Other Type Input -->
					<div
						v-if="state.responsibleIdentificationDocumentType == 'O' && showResponsible"
						class="col-span-12 md:col-span-4 md:col-start-6">
						<CustomInput
							type="text"
							:label="t('identificationDocument.otherType')"
							:name="'responsibleOtherIdentificationDocumentType'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleOtherIdentificationDocumentType"
							:error="''"
							@value-changed="
								(option) =>
									(state.responsibleOtherIdentificationDocumentType = option)
							" />
					</div>
					<!-- Athlete's Responsible Identification Document Number Input -->
					<div v-if="showResponsible" class="col-span-12 md:col-span-3 md:col-start-1">
						<CustomInput
							type="text"
							:label="t('identificationDocument.number')"
							:name="'responsibleIdentificationDocumentNumber'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleIdentificationDocumentNumber"
							:error="''"
							@value-changed="
								(option) => (state.responsibleIdentificationDocumentNumber = option)
							" />
					</div>
					<!-- Athlete's Responsible Identification Document Emitted By Input -->
					<div
						v-if="state.responsibleIdentificationDocumentType != 'C' && showResponsible"
						class="col-span-12 md:col-span-3">
						<CustomInput
							type="text"
							:label="t('identificationDocument.emitedBy')"
							:name="'responsibleIdentificationDocumentEmittedBy'"
							:readonly="!canEdit.private"
							:option-selected="state.responsibleIdentificationDocumentEmittedBy"
							:error="''"
							@value-changed="
								(option) =>
									(state.responsibleIdentificationDocumentEmittedBy = option)
							" />
					</div>
					<!-- Athlete's Responsible Identification Document Expiration Date Input -->
					<div v-if="showResponsible" class="col-span-12 md:col-span-3">
						<DateInput
							:label="t('identificationDocument.expirationDate')"
							:readonly="!canEdit.private"
							:name="'responsibleIdentificationDocumentExpirationDate'"
							:option-selected="state.responsibleIdentificationDocumentExpirationDate"
							:error="''"
							@value-changed="
								(option) =>
									(state.responsibleIdentificationDocumentExpirationDate = option)
							" />
					</div>
				</FormAthlete>
				<!-- Private Information Form -->
				<FormAthlete
					v-if="store.getters.getUserRole == 'ADMIN'"
					id="privateInformationForm"
					:title="t('label.information.admin.title')"
					:subtitle="t('label.information.admin.sub')"
					:button-save="t('saveButton')"
					:button-edit="t('editButton')"
					:can-edit="canEdit.admin"
					@submited="isEdit ? editAthlete('admin') : createAthlete()"
					@edit="canEdit.admin = true">
					<div class="col-span-12 md:col-span-9">
						<TextArea
							name="notes"
							:label="t('form.notes')"
							:option-selected="state.notes"
							:error="''"
							:readonly="!canEdit.admin"
							@value-changed="(option) => (state.notes = option)" />
					</div>
				</FormAthlete>

				<!-- Insurance Form -->
				<div
					v-if="store.getters.getUserRole == 'ADMIN' && isEdit"
					id="insuranceInformationForm"
					class="scroll-mt-44">
					<div class="shadow md:overflow-hidden md:rounded-md">
						<div class="space-y-6 bg-white py-6 px-4 md:p-6">
							<div>
								<h3 class="text-lg font-medium leading-6 text-gray-900">
									{{ t("label.information.insurance.title") }}
								</h3>
								<p class="mt-1 text-md text-gray-500">
									{{ t("label.information.insurance.sub") }}
								</p>
							</div>
							<p
								v-if="
									athlete.insured_entity == null ||
									athlete.insured_entity.insurances.length == 0
								"
								class="text-xl font-medium text-center">
								{{ t("noInsurances") }}
							</p>
							<div v-else class="space-y-2">
								<div
									v-for="insurance of athlete.insured_entity.insurances"
									:key="insurance.id">
									<div
										class="w-full grid grid-cols-3 bg-blue-100 rounded-full px-8 py-2">
										<p
											class="col-span-full text-center lg:text-left lg:col-span-1">
											{{
												insurance.insurance_group != null
													? t("insurance.group", {
															group: insurance.insurance_group.name,
													  })
													: t("insurance.noGroup")
											}}
										</p>
										<p class="col-span-full text-center lg:col-span-1">
											{{
												t("insurance.type", {
													type: insurance.insurance_type.name,
												})
											}}
										</p>
										<p
											class="col-span-full text-center lg:text-right lg:col-span-1 min-w-max">
											{{
												t("insurance.date", {
													dateStart: translateDateFromApi(
														insurance.start_date
													),
													dateEnd: translateDateFromApi(
														insurance.end_date
													),
												})
											}}
										</p>
										<div
											v-if="
												!!athlete.user_id && insurance.coach_certificate_url
											"
											class="min-w-max inline-flex gap-x-2 col-span-full justify-center">
											<a
												class="min-w-max link"
												target="_blank"
												:href="
													'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
													insurance.coach_certificate_url
												">
												{{ t("seeCoachCertificate") }}
											</a>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import InsuranceModal from "@/components/admin/modals/insurance.vue";
import Button from "@/components/partials/button.vue";
import ImageInput from "@/components/partials/inputs/imageInput.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import DateInput from "@/components/partials/inputs/dateInput.vue";
import RadioGroup from "@/components/partials/inputs/radioGroup.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import {
	default as TextArea,
	default as TextAreaInput,
} from "@/components/partials/inputs/textAreaInput.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import Loading from "@/components/partials/loading.vue";
import FormAthlete from "@/components/partials/templates/formAthlete.vue";
import router from "@/router";
import { authApi, errorHandling, translateDateFromApi } from "@/services/api";
import store from "@/store";
import toast from "@/toast.js";
import { KeyIcon, SquaresPlusIcon, UserCircleIcon } from "@heroicons/vue/24/outline";
import { useVuelidate } from "@vuelidate/core";
import { helpers, required } from "@vuelidate/validators";
import e from "countries-list";
import c from "country-list";
import { computed, ref, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useRoute } from "vue-router";

const { path } = useRoute();
let { t } = useI18n();

const props = defineProps({
	athleteId: {
		type: String,
		required: false,
		default: "0",
	},
	teamId: {
		type: String,
		required: false,
		default: "0",
	},
});

let navigation = ref([
	{
		name: t("nav.public"),
		href: "#publicInformationForm",
		icon: UserCircleIcon,
		current: true,
		show: true,
	},
	{
		name: t("nav.private"),
		href: "#privateInformationForm",
		icon: KeyIcon,
		current: false,
		show: true,
	},
]);
if (store.getters.getUserRole == "ADMIN") {
	navigation.value.push({
		name: t("nav.insurance"),
		href: "#insuranceInformationForm",
		icon: SquaresPlusIcon,
		current: false,
	});
}
const regions = ref([
	{
		name: t("form.regions.north"),
		id: "north",
	},
	{
		name: t("form.regions.center"),
		id: "center",
	},
	{
		name: t("form.regions.south"),
		id: "south",
	},
]);
let athlete = ref({});
let loading = ref(true);
let initialLoading = ref(true);
let loadingForm = ref(false);
let isEdit = ref(props.athleteId != "0");
let canEdit = ref({
	public: !isEdit.value,
	private: !isEdit.value,
	admin: !isEdit.value,
	team: props.teamId == "0",
});
let openModal = ref(false);
let modalInsuranceId = ref("");
let belts = ref([]);
let teams = ref([]);
let todayDate = new Date();
let state = ref({
	name: "",
	isMale: "",
	weight: "",
	isAdapted: false,
	birthday: "",
	team: props.teamId,
	belt: "",

	email: "",
	phone: "",
	nationality: "",
	naturalityRegion: "",
	naturalityCountry: "",
	genderIsMale: "",
	federationNumber: "",
	federationActive: false,
	nif: "",

	identificationDocumentType: "",
	otherIdentificationDocumentType: "",
	identificationDocumentNumber: "",
	identificationDocumentEmittedBy: "",
	identificationDocumentExpirationDate: "",

	address: "",
	zipCode: "",
	city: "",
	district: "",
	region: "",
	country: "",

	responsibleName: "",
	responsibleRelationship: "",
	responsibleEmail: "",

	responsibleIidentificationDocumentType: "",
	responsibleOtherIdentificationDocumentType: "",
	responsibleIdentificationDocumentNumber: "",
	responsibleIdentificationDocumentEmittedBy: "",
	responsibleIdentificationDocumentExpirationDate: "",
});
const newImg = ref(null);
const imageUrl = computed(() =>
	athlete.value.profile_picture_url
		? `https://kempo-files.fra1.digitaloceanspaces.com/${athlete.value.profile_picture_url}`
		: ""
);

let n = c.getCodeList();
let keys = Object.keys(n);
let countries = ref([]);
keys.forEach((key) => {
	countries.value.push({
		id: key.toUpperCase(),
		name: e.getEmojiFlag(key.toUpperCase()) + " " + n[key],
	});
});

const req = helpers.withMessage(t("error.required"), required);
const competitionGenderReq = helpers.withMessage(t("error.required"), (value) =>
	state.value.isMale == "O" ? value.includes("M") || value.includes("F") : true
);
let rules = {
	name: { req: req },
	isAdapted: { req: req },
};
if (store.getters.getUserRole == "COACH") {
	rules.belt = {};
	rules.belt.req = req;
	rules.weight = {};
	rules.weight.req = req;
	rules.isMale = {};
	rules.isMale.req = competitionGenderReq;
	rules.genderIsMale = {};
	rules.genderIsMale.req = req;
	rules.birthday = {};
	rules.birthday.req = req;
}
let v$ = useVuelidate(rules, state, { $scope: "athlete" });
let showResponsible = computed(() => {
	if (state.value.birthday == null || state.value.birthday == "") return true;
	if (typeof state.value.birthday == "string") {
		return Number(state.value.birthday.split("-")[2]) + 18 > todayDate.getFullYear();
	}
	return state.value.birthday.getFullYear() + 18 > todayDate.getFullYear();
});

let initialPromises = [];
initialPromises.push(
	authApi.get("belts").then(({ data }) => {
		belts.value = data.map((belt) => ({ name: `belts.${belt.name}`, id: belt.id }));
		belts.value.push({ id: "", name: "belts.ungraduated" });
	})
);

initialPromises.push(
	authApi.get("teams").then(({ data }) => {
		teams.value = data;
		teams.value = teams.value.map((team) => ({
			id: team.id,
			name: `${team.name}${team.abbreviation ? ` (${team.abbreviation})` : ""}`,
		}));
		teams.value.push({ id: "0", name: t("noTeam") });
	})
);

Promise.all(initialPromises)
	.then(() => {
		initialLoading.value = false;
	})
	.catch((error) => {
		errorHandling(error);
	});

let allLoaded = computed(() => !loading.value && !initialLoading.value);
let observer = null;
let sections = [];
let config = null;

// Scroll observer
watch(
	() => allLoaded.value,
	async () => {
		await setTimeout(null, 100);
		if (observer != null) return;
		config = {
			rootMargin: "0px",
			threshold: [0.2],
		};

		sections = [
			document.getElementById("publicInformationForm"),
			document.getElementById("privateInformationForm"),
		];
		if (store.getters.getUserRole == "ADMIN") {
			sections.push(document.getElementById("insuranceInformationForm"));
		}

		observer = new IntersectionObserver(function (entries) {
			entries.forEach((entry) => {
				if (entry.isIntersecting) {
					for (let nav of navigation.value) {
						nav.current = `#${entry.target.id}` == nav.href;
					}
				}
			});
		}, config);

		sections.forEach((section) => {
			observer.observe(section);
		});
	}
);

function getAthlete(atId) {
	if (atId == "0") {
		loading.value = false;
		loadingForm.value = false;
		return;
	}
	loadingForm.value = true;
	authApi
		.get(`athletes/${atId}`)
		.then(({ data }) => {
			setAthlete(data);
			loading.value = false;
			loadingForm.value = false;
		})
		.catch((error) => {
			errorHandling(error);
		});
}
getAthlete(props.athleteId);

function setAthlete(responseData) {
	athlete.value = responseData;
	state.value.name = responseData.name || "";
	state.value.team = responseData.team_id || "";
	state.value.federationActive = responseData.private_info.federation_active || false;
	state.value.federationNumber = responseData.private_info.federation_number || null;
	state.value.belt = responseData.belt_id || "";
	state.value.weight = responseData.weight || 0;
	state.value.birthday = translateDateFromApi(responseData.birthday) || "";
	state.value.isAdapted = responseData.is_adapted || false;
	state.value.genderIsMale = responseData.private_info.gender_is_male || "";
	state.value.isMale = responseData.is_male == null ? "" : responseData.is_male ? "M" : "F";
	state.value.email = responseData.private_info.email || "";
	state.value.phone = responseData.private_info.phone_number || "";
	state.value.nationality = responseData.private_info.nationality || "";
	state.value.naturalityRegion = responseData.private_info.naturality_region || "";
	state.value.naturalityCountry = responseData.private_info.naturality_country || "";
	if (responseData.private_info.identification_document.type != null) {
		if (
			["C", "B", "I", "P"].indexOf(responseData.private_info.identification_document.type) ==
			-1
		) {
			state.value.identificationDocumentType = "O";
			state.value.otherIdentificationDocumentType =
				responseData.private_info.identification_document.type || "";
		} else {
			state.value.identificationDocumentType =
				responseData.private_info.identification_document.type || "";
			state.value.otherIdentificationDocumentType = "";
		}
	}
	state.value.identificationDocumentNumber =
		responseData.private_info.identification_document.number || "";
	state.value.identificationDocumentEmittedBy =
		responseData.private_info.identification_document.emitted_by || "";
	state.value.identificationDocumentExpirationDate =
		translateDateFromApi(responseData.private_info.identification_document.expiration_date) ||
		"";
	state.value.nif = responseData.private_info.nif || "";
	state.value.address = responseData.address.address || "";
	state.value.zipCode = responseData.address.zip_code || "";
	state.value.region = responseData.address.region || "";
	state.value.country = responseData.address.country || "";
	state.value.responsibleName = responseData.responsible.name || "";
	state.value.responsibleEmail = responseData.responsible.email || "";
	state.value.responsibleRelationship = responseData.responsible.relationship || "";
	if (responseData.responsible.identification_document.type != null) {
		if (
			["C", "B", "I", "P"].indexOf(responseData.responsible.identification_document.type) ==
			-1
		) {
			state.value.responsibleIdentificationDocumentType = "O";
			state.value.responsibleOtherIdentificationDocumentType =
				responseData.responsible.identification_document.type || "";
		} else {
			state.value.responsibleIdentificationDocumentType =
				responseData.responsible.identification_document.type || "";
			state.value.otherIdentificationDocumentType = "";
		}
	}
	state.value.responsibleIdentificationDocumentNumber =
		responseData.responsible.identification_document.number || "";
	state.value.responsibleIdentificationDocumentEmittedBy =
		responseData.responsible.identification_document.emitted_by || "";
	state.value.responsibleIdentificationDocumentExpirationDate =
		translateDateFromApi(responseData.responsible.identification_document.expiration_date) ||
		"";
	state.value.notes = responseData.notes;
}

const saveProfilePictureToSaveLater = async (file) => {
	newImg.value = file;
};

async function editAthlete(formTitle) {
	loadingForm.value = true;
	if (formTitle == "all" || formTitle == "public") {
		let isFormValid = await v$.value.$validate();
		if (!isFormValid) {
			toast.error(t("error.invalidData"));
			loadingForm.value = false;
			return;
		}
	}

	let promises = [];
	if (formTitle == "all" || formTitle == "public") {
		let publicData = {
			name: state.value.name,
			team_id: state.value.team == "0" ? null : state.value.team,
			belt_id: state.value.belt,
			weight: state.value.weight,
			birthday: state.value.birthday,
			is_adapted: state.value.isAdapted,
			is_male:
				state.value.genderIsMale == "O"
					? state.value.isMale == "M"
					: state.value.genderIsMale == "M",
		};

		promises.push(authApi.put(`athletes/${athlete.value.id}`, publicData));
		if (formTitle != "all") {
			promises.push(
				authApi.put(`private-info/${athlete.value.private_info_id}`, {
					gender_is_male: state.value.genderIsMale,
				})
			);
		}
		if (newImg.value != null) {
			const formData = new FormData();
			formData.append("file", newImg.value);
			promises.push(
				authApi.put(`athletes/${athlete.value.id}/profile-picture`, formData, {
					headers: { "Content-Type": "multipart/form-data" },
				})
			);
		}
	}
	if (formTitle == "all" || formTitle == "private") {
		let privateData = {
			gender_is_male: state.value.genderIsMale,
			federation_active: state.value.federationActive,
			federation_number: Number(state.value.federationNumber) || null,
			email: state.value.email,
			phone_number: state.value.phone,
			nationality: state.value.nationality,
			naturality_region: state.value.naturalityRegion,
			naturality_country: state.value.naturalityCountry,
			nif: state.value.nif,
		};
		promises.push(authApi.put(`private-info/${athlete.value.private_info_id}`, privateData));

		let identificationDocumentData = {
			type:
				state.value.identificationDocumentType == "O"
					? state.value.otherIdentificationDocumentType
					: state.value.identificationDocumentType,
			number: state.value.identificationDocumentNumber,
			expiration_date: state.value.identificationDocumentExpirationDate,
			emitted_by: state.value.identificationDocumentEmittedBy,
		};

		promises.push(
			authApi.put(
				`identification-documents/${athlete.value.private_info.identification_document_id}`,
				identificationDocumentData
			)
		);

		let addressData = {
			address: state.value.address,
			city: state.value.city,
			zip_code: state.value.zipCode,
			district: state.value.district,
			region: state.value.region,
			country: state.value.country,
		};

		promises.push(authApi.put(`addresses/${athlete.value.address_id}`, addressData));

		let responsibleData = {
			name: state.value.responsibleName,
			email: state.value.responsibleEmail,
			relationship: state.value.responsibleRelationship,
		};

		promises.push(authApi.put(`responsible/${athlete.value.responsible_id}`, responsibleData));

		let responsibleIdentificationDocumentData = {
			type:
				state.value.responsibleIdentificationDocumentType == "O"
					? state.value.responsibleOtherIdentificationDocumentType
					: state.value.responsibleIdentificationDocumentType,
			number: state.value.responsibleIdentificationDocumentNumber,
			expiration_date: state.value.responsibleIdentificationDocumentExpirationDate,
			emitted_by: state.value.responsibleIdentificationDocumentEmittedBy,
		};

		promises.push(
			authApi.put(
				`identification-documents/${athlete.value.responsible.identification_document_id}`,
				responsibleIdentificationDocumentData
			)
		);
	}

	if (formTitle == "all" || formTitle == "admin") {
		promises.push(
			authApi.patch(`athletes/${athlete.value.id}/notes`, { notes: state.value.notes })
		);
	}

	Promise.all(promises)
		.then(() => {
			authApi.get(`athletes/${athlete.value.id}`).then((response) => {
				setAthlete(response.data);
				canEdit.value.public = false;
				canEdit.value.private = false;
				canEdit.value.admin = false;
				loadingForm.value = false;
				newImg.value = null;
			});
		})
		.catch((error) => {
			console.log(error);
			errorHandling(error);
			loadingForm.value = false;
		});
}

async function createAthlete() {
	loadingForm.value = true;

	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		toast.error(t("error.invalidData"));
		loadingForm.value = false;
		return;
	}

	let publicData = {
		name: state.value.name,
		team_id: state.value.team == "0" ? null : state.value.team,
		belt_id: state.value.belt || null,
		weight: state.value.weight || null,
		birthday: state.value.birthday,
		is_adapted: state.value.isAdapted,
		is_male:
			state.value.genderIsMale == "O"
				? state.value.isMale == "M"
				: state.value.genderIsMale == "M",
		notes: state.value.notes,
	};
	let privateData = {
		gender_is_male: state.value.genderIsMale,
		federation_active: state.value.federationActive,
		federation_number: state.value.federationNumber || null,
		email: state.value.email,
		phone_number: state.value.phone,
		nationality: state.value.nationality,
		naturality_region: state.value.naturalityRegion,
		naturality_country: state.value.naturalityCountry,
		nif: state.value.nif,
	};

	let identificationDocumentData = {
		type:
			state.value.identificationDocumentType == "O"
				? state.value.otherIdentificationDocumentType
				: state.value.identificationDocumentType,
		number: state.value.identificationDocumentNumber,
		expiration_date: state.value.identificationDocumentExpirationDate,
		emitted_by: state.value.identificationDocumentEmittedBy,
	};

	let addressData = {
		address: state.value.address,
		city: state.value.city,
		zip_code: state.value.zipCode,
		district: state.value.district,
		region: state.value.region,
		country: state.value.country,
	};

	let responsibleData = {
		name: state.value.responsibleName,
		email: state.value.responsibleEmail,
		relationship: state.value.responsibleRelationship,
	};

	let responsibleIdentificationDocumentData = {
		type:
			state.value.responsibleIdentificationDocumentType == "O"
				? state.value.responsibleOtherIdentificationDocumentType
				: state.value.responsibleIdentificationDocumentType,
		number: state.value.responsibleIdentificationDocumentNumber,
		expiration_date: state.value.responsibleIdentificationDocumentExpirationDate,
		emitted_by: state.value.responsibleIdentificationDocumentEmittedBy,
	};

	authApi
		.post(`athletes`, {
			public_data: publicData,
			private_data: privateData,
			responsible: responsibleData,
			address: addressData,
			identification: identificationDocumentData,
			identification_responsible: responsibleIdentificationDocumentData,
		})
		.then(async (response) => {
			let data = response.data;
			if (newImg.value != null) {
				const formData = new FormData();
				formData.append("file", newImg.value);
				const response2 = await authApi.put(
					`athletes/${data.id}/profile-picture`,
					formData,
					{
						headers: { "Content-Type": "multipart/form-data" },
					}
				);
				data = response2.data;
			}
			setAthlete(data);
			let newRoute = path.split("/");
			newRoute.pop();
			newRoute = `${newRoute.join("/")}/${data.id}`;
			router.replace(`${newRoute}`);
			canEdit.value.public = false;
			canEdit.value.private = false;
			canEdit.value.admin = false;
			loadingForm.value = false;
			isEdit.value = true;
		})
		.catch((error) => {
			console.log(error);
			errorHandling(error);
			loadingForm.value = false;
		});
}

async function deleteInsurance(insuranceId) {
	loadingForm.value = true;
	authApi
		.delete(`insurances/${insuranceId}`)
		.then(() => {
			getAthlete(props.athleteId);
		})
		.catch((error) => {
			loadingForm.value = false;
			errorHandling(error);
		});
}
</script>

<i18n>
{
	"en_GB": {
		"titleModal": "Atlhete already created!",
		"warning": "Most of the athletes are already created but not all were able to be associated with the respective teams, if you want to add new athletes to your team please send an email to ",
		"warning1": "with the name of the team in question, the name of the athletes you want to add, their age and if you know it the number of federation.",
		"filter": {
			"name": "Filter by Name",
			"clear": "Clear Filters",
		},
		"form": {
			"profilePicture": "Profile picture",
			"name": "Name",
			"weight": "Weight (Kg.)",
			"birthday": "Birthday",
			"belt": "Belt",
			"team": "Athlete's Team",
			"federationActive": "Athlete is Federated",
			"federationNumber": "Athlete's Federated Number",
			"genderIsMale": "Gender",
			"isMale": "Gender in the Competition",
			"isAdapted": "Adapted",
			"email": "Email Address",
			"phone": "Phone Number",
			"nationality": "Nationality",
			"naturalityRegion": "Naturality Region",
			"naturalityCountry": "Naturality Country",
			"responsible": {
				"name": "Name",
				"relationship": "Relationship with the Athlete",
				"email": "Email",
				"identificationDocumentNumber": "Number of the Document of Identification",
				"identificationDocumentExpirationDate": "Expiration date of the Document of Identification"
			},
			"nif": "NIF",
			"address": "Address",
			"city": "City/Locality",
			"district": "District",
			"region": "Region",
			"regions": {
				"north": "North",
				"center": "Center",
				"south": "South"
			},
			"zipCode": "Zip-Code",
			"country": "Country",
			"notes": "Notes",
		},
		"title": {
			"address": "Athlete's Address",
			"responsible": "Athlete's Responsible"
		},
		"nav": {
			"public": "Public Information",
			"private": "Private Information",
			"insurance": "Insurance Information",
		},
		"error": {
			"required": "Cannot be empty",
			"invalidData": "Invalid Data"
		},
		"label": {
			"information": {
				"public": {
					"title": "Athlete's Public Information",
					"sub": "This information is available for the general public"
				},
				"private": {
					"title": "Athlete's Private Information",
					"sub": "This information is only available for the admins and the athlete's coach"
				},
				"insurance": {
					"title": "Athlete's Insurance Information",
					"sub": "This information is only available for the admins"
				},
				"admin": {
					"title": "Admin Information",
					"sub": "This information is only available for the admins"
				},
			},
		},
		"insurance": {
			"noGroup": "No Insurance Group",
			"group": "Group: {group}",
			"type": "Type: {type}",
			"date": "From {dateStart} to {dateEnd}",
			"edit": "Edit",
			"delete": "Delete"
		},
		"createFirst": "Create the Athlete First",
		"noInsurances": "This Atlhete has no insurances yet",
		"createInsurance": "Create a new Insurance",
		"saveButton": "Save",
		"editButton": "Edit",
		"masc": "Masculine",
		"fem": "Feminine",
		"other": "Other",
		"noTeam": "No Team",
		"notFederated": "Not Federated",
		"imageUpdated": "Image updated!"
	},
	"pt_PT": {
		"titleModal": "Atleta já criado!",
		"warning": "A maior parte dos atletas já se encontram na plataforma mas não foi possível associar todos às respetivas equipas, se pretende adicionar novos atletas à sua equipa por favor envie um email para ",
		"warning1": "com o nome da equipa em questão, o nome dos atletas que pretende adicionar a idade de cada um e o número de federado caso o saiba",
		"filter": {
			"name": "Filtrar Por Nome",
			"clear": "Limpar Filtros",
		},
		"form": {
			"profilePicture": "Imagem de perfil",
			"name": "Nome",
			"weight": "Peso (Kg.)",
			"birthday": "Data de Nascimento",
			"belt": "Cinto",
			"team": "Equipa do Atleta",
			"federationActive": "Atleta é Federado",
			"federationNumber": "Número de Federado do Atleta",
			"genderIsMale": "Género",
			"isMale": "Género na Competição",
			"isAdapted": "Adaptado",
			"email": "Endereço de Email",
			"phone": "Número de Telemóvel",
			"nationality": "Nationalidade",
			"naturalityRegion": "Natural da Região",
			"naturalityCountry": "Natural do País",
			"responsible": {
				"name": "Nome",
				"relationship": "Relação com o Atleta",
				"email": "Email"
			},
			"nif": "NIF",
			"address": "Morada",
			"city": "Localidade",
			"district": "Distrito",
			"region": "Região",
			"regions": {
				"north": "Norte",
				"center": "Centro",
				"south": "Sul"
			},
			"zipCode": "Código Postal",
			"country": "País",
			"notes": "Notas",
		},
		"title": {
			"address": "Morada do Atleta",
			"responsible": "Encarregado de Educação do Atleta"
		},
		"nav": {
			"public": "Informação Pública",
			"private": "informação Privada",
			"insurance": "Informação do Seguro",
		},
		"error": {
			"required": "Não pode estar vazio",
			"invalidData": "Dados inválidos"
		},
		"label": {
			"information": {
				"public": {
					"title": "Informação Pública do Atleta",
					"sub": "Esta informação é acessível ao público geral"
				},
				"private": {
					"title": "Informação Privada do Atleta",
					"sub": "Esta informação é apenas acessível aos Admins e ao treinador do atleta"
				},
				"insurance": {
					"title": "Informação do Seguro do Atleta",
					"sub": "Esta informação é apenas acessível aos Admins"
				},
				"admin": {
					"title": "Informação dos Admins",
					"sub": "Esta informação é apenas acessível aos Admins"
				},
			},
		},
		"insurance": {
			"noGroup": "Sem Grupo de Seguro",
			"group": "Grupo: {group}",
			"type": "Tipo: {type}",
			"date": "De {dateStart} até {dateEnd}",
			"edit": "Editar",
			"delete": "Apagar"
		},
		"createFirst": "Crie o Atleta Primeiro",
		"noInsurances": "Este Atleta ainda não tem nenhum Seguro",
		"createInsurance": "Criar um novo Seguro",
		"saveButton": "Guardar",
		"editButton": "Editar",
		"masc": "Masculino",
		"fem": "Feminino",
		"other": "Outro",
		"noTeam": "Sem Equipa",
		"notFederated": "Não Federado",
		"imageUpdated": "Imagem atualizada!"
	}
}
</i18n>
