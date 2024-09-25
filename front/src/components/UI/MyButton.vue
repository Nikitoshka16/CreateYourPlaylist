<template>
    <button class="btn">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: 'my-button'
}
</script>

<style scoped>
.btn{
    border-radius: 8px;
    margin: 1em;
    padding: 10px 15px;
    background: none;
    color:#61f798;
    border: 1px solid #61f798;
}
</style>