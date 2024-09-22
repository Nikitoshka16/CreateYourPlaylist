<template>
    <input class="input"
           :value="modelValue"
           @input="$emit('update:modelValue', $event.target.value)"
           :type="isPassword"
    />
</template>

<script>
export default {
    props: {
        modelValue: {
            required: true,
            type: String
        },
        isPassword: {
            required: false,
            type: String,
            default: "text"
        }
    }
}
</script>

<style scoped>
.input{
    width: 100%;
    border: 1px solid teal;
    padding: 10px 15px;
    margin-top: 15px;
}
</style>