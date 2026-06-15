<template>
  <div class="intelligent-search">
    <!-- Float button -->
    <div class="ai-float-btn" @click="visible = !visible" v-if="!visible">
      <i class="el-icon-s-custom"></i>
      <span>{{ $t('smart.assistant') }}</span>
    </div>
    <!-- Chat panel -->
    <el-drawer
      :visible.sync="visible"
      direction="rtl"
      size="420px"
      :title="$t('smart.assistant')"
      :before-close="handleClose"
    >
      <div class="ai-chat-panel">
        <!-- Messages area -->
        <div class="chat-messages" ref="chatMessages">
          <!-- Welcome message -->
          <div class="chat-message assistant">
            <div class="message-avatar">
              <i class="el-icon-cpu"></i>
            </div>
            <div class="message-bubble">
              <p>{{ $t('smart.welcome') }}</p>
              <p style="color:#909399;font-size:12px;margin-top:8px;">{{ $t('smart.example1') }}</p>
              <p style="color:#909399;font-size:12px;">{{ $t('smart.example2') }}</p>
            </div>
          </div>
          <!-- Chat messages -->
          <div v-for="(msg, i) in messages" :key="i" :class="['chat-message', msg.role]">
            <div class="message-avatar">
              <i :class="msg.role === 'user' ? 'el-icon-user' : 'el-icon-cpu'"></i>
            </div>
            <div class="message-body">
              <div class="message-bubble" v-html="formatMessage(msg.content)"></div>
              <!-- Action buttons -->
              <div v-if="msg.actions && msg.actions.length" class="message-actions">
                <el-button
                  v-for="(act, j) in msg.actions"
                  :key="j"
                  size="mini"
                  :icon="act.icon"
                  @click="navigateTo(act.path)"
                >{{ act.text }}</el-button>
              </div>
            </div>
          </div>
          <!-- Typing indicator -->
          <div v-if="typing" class="chat-message assistant">
            <div class="message-avatar">
              <i class="el-icon-cpu"></i>
            </div>
            <div class="message-bubble typing-bubble">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </div>
          </div>
        </div>
        <!-- Input area -->
        <div class="chat-input">
          <el-input
            v-model="inputText"
            :placeholder="$t('smart.placeholder')"
            @keyup.enter.native="sendMessage"
            size="small"
            :disabled="typing"
          >
            <el-button
              slot="append"
              icon="el-icon-s-promotion"
              @click="sendMessage"
              :loading="typing"
            ></el-button>
          </el-input>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import { sendAiMessage } from '@/api'

export default {
  name: 'IntelligentSearch',
  data() {
    return {
      visible: false,
      inputText: '',
      messages: [],
      typing: false
    }
  },
  methods: {
    async sendMessage() {
      const text = this.inputText.trim()
      if (!text || this.typing) return

      this.messages.push({ role: 'user', content: text })
      this.inputText = ''
      this.$nextTick(() => this.scrollToBottom())

      // Call AI API
      this.typing = true
      try {
        const history = this.messages
          .filter(m => m.role !== 'system')
          .slice(-10)
          .map(m => ({ role: m.role, content: m.content }))

        const res = await sendAiMessage({ message: text, history })
        const data = res.data

        this.messages.push({
          role: 'assistant',
          content: data.reply,
          actions: data.actions || []
        })
      } catch (e) {
        this.messages.push({
          role: 'assistant',
          content: '抱歉，我暂时无法处理您的请求。请稍后再试或联系管理员。'
        })
      }
      this.typing = false
      this.$nextTick(() => this.scrollToBottom())
    },
    formatMessage(content) {
      if (!content) return ''
      // Convert newlines to <br>, bold markers
      return content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    },
    navigateTo(path) {
      if (!path) return
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
      this.visible = false
    },
    handleClose() {
      this.visible = false
    },
    scrollToBottom() {
      const el = this.$refs.chatMessages
      if (el) el.scrollTop = el.scrollHeight
    }
  }
}
</script>

<style scoped>
.ai-float-btn {
  position: fixed;
  right: 20px;
  bottom: 80px;
  z-index: 99;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #1a4a80;
  color: #fff;
  padding: 10px 18px;
  border-radius: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(26, 74, 128, 0.4);
  transition: all 0.3s;
  font-size: 14px;
}
.ai-float-btn:hover {
  background: #2d5d9d;
  transform: translateY(-2px);
}
.ai-chat-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}
.chat-message {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}
.chat-message.user {
  flex-direction: row-reverse;
}
.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #ebeef5;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 18px;
}
.chat-message.assistant .message-avatar {
  background: #e6f0fa;
  color: #1a4a80;
}
.chat-message.user .message-avatar {
  background: #1a4a80;
  color: #fff;
}
.message-body {
  max-width: 85%;
}
.message-bubble {
  padding: 10px 14px;
  border-radius: 12px;
  background: #f0f2f5;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}
.chat-message.user .message-bubble {
  background: #1a4a80;
  color: #fff;
}
.message-actions {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.chat-input {
  padding: 12px 16px;
  border-top: 1px solid #ebeef5;
}
/* Typing indicator */
.typing-bubble {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 12px 16px;
}
.typing-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #909399;
  animation: typing-bounce 1.4s infinite ease-in-out both;
}
.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40% { transform: translateY(-6px); opacity: 1; }
}
</style>
