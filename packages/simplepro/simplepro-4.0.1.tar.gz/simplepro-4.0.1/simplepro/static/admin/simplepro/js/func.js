//处理自定义方法字段和对话框、和共用组件

Vue.component('HtmlRender', {
    props: ['html'],
    mounted() {
        //调用vue来渲染
        try {
            let res = Vue.compile(`<div class="cell-btn">${this.html}<slot></slot></div>`);
            new Vue({
                el: this.$el,
                render: res.render,
                staticRenderFns: res.staticRenderFns
            });
        } catch (e) {
            console.warn(`Data can only be displayed as text`);
        }
    },
    template: `<div ref="el" v-html="html"></div>`

});

Vue.component('ModalDialog', {
    props: ['data'],
    data() {
        return {
            visible: false,
        }
    },
    watch: {
        visible(val) {
            if (val) {
                window.currentModal = this;
            }
        }
    },
    methods: {
        showDialog() {
            console.log('showDialog')
            this.visible = true;
        },
        close() {
            this.visible = false;
        }
    },
    template: `
        <div>
        <div @click="showDialog()">
            <HtmlRender :html="data.cell"/>
        </div>
        <el-dialog
          :title="data.title"
          :visible.sync="visible"
          :width="data.width">
          <div :style="{height:data.height,overflow:'auto'}" v-cloak>
            
            <iframe v-if="visible&&data.url" :src="data.url" frameborder="0" width="100%" height="100%"></iframe>
            <el-alert v-if="visible&&!data.url" type="error" title="请设置ModalDialog的url"></el-alert>
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button v-if="data.show_cancel" size="small" @click="visible = false">取 消</el-button>
          </span>
        </el-dialog>
        </div>
    `
});

Vue.component('func', {
    props: ['value'],
    computed: {
        isArrayDialog() {
            return this.value._type === 'MultipleCellDialog';
        },
        isDialog() {
            return typeof this.value == 'object';
        }
    },
    template: `
    <div v-if="isArrayDialog" style="display: flex;justify-content: space-around;">
        <ModalDialog v-for="item in value.modals" :key="item" :data="item"></ModalDialog>
    </div>
    <ModalDialog v-else-if="isDialog&&value._type=='ModalDialog'" :data="value"></ModalDialog>
    <HtmlRender v-else :html="value"/>
    `
});

//渲染layer的组件
Vue.component('layer', {
    props: ['value'],
    render(h) {
        return h('div', {
            domProps: {
                innerHTML: this.value
            }
        });
    }
});