import { Component, ViewChild, ElementRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent {
  isOpen = false;
  userInput: string = '';
  messages: { text: string, sender: string, audio?: string, isPlaying?: boolean, isPaused?: boolean }[] = [];
  recognition: any;
  isRecording = false;
  audioPlayer = new Audio();
  currentPlayingMessage: any = null;

  @ViewChild('chatBody') chatBody!: ElementRef;

  constructor(private http: HttpClient) {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.continuous = false;
    this.recognition.lang = 'en-US';

    // Auto-send voice input
    this.recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      this.userInput = transcript;
      this.sendMessage();
    };

    this.recognition.onend = () => {
      this.isRecording = false;
    };

    this.recognition.onerror = (event: any) => {
      console.error("Speech recognition error:", event);
      this.isRecording = false;
    };
  }

  toggleChatbot() {
    this.isOpen = !this.isOpen;
  }

  sendMessage() {
    if (!this.userInput.trim()) return;

    this.messages.push({ text: this.userInput, sender: 'user' });
    this.scrollToBottom();

    this.http.post<{ reply: string, audio_url: string }>('http://localhost:5000/chat', { message: this.userInput }).subscribe(
      response => {
        this.messages.push({ text: response.reply, sender: 'bot', audio: response.audio_url });
        this.scrollToBottom();
      }
    );

    this.userInput = '';
  }

  startRecording() {
    this.isRecording = true;
    this.recognition.start();
  }

  stopRecording() {
    this.isRecording = false;
    this.recognition.stop();
  }

  toggleAudio(msg: any) {
    // Stop any currently playing audio
    if (this.currentPlayingMessage && this.currentPlayingMessage !== msg) {
      this.currentPlayingMessage.audioPlayer.pause();
      this.currentPlayingMessage.isPlaying = false;
      this.currentPlayingMessage.isPaused = false;
    }
  
    // If audio already exists, toggle play/pause
    if (msg.audioPlayer) {
      if (msg.isPlaying) {
        msg.audioPlayer.pause();
        msg.isPlaying = false;
        msg.isPaused = true;
      } else {
        msg.audioPlayer.play();
        msg.isPlaying = true;
        msg.isPaused = false;
      }
      this.currentPlayingMessage = msg;
      return;
    }
  
    // Create a new SpeechSynthesisUtterance instance for unique audio
    const speechSynthesis = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(msg.text);
  
    // Play text-to-speech
    speechSynthesis.speak(utterance);
  
    // Create an audio player
    msg.audioPlayer = new Audio();
    msg.isPlaying = true;
    msg.isPaused = false;
    this.currentPlayingMessage = msg;
  
    // Stop the audio when speech ends
    utterance.onend = () => {
      msg.isPlaying = false;
      msg.isPaused = false;
      this.currentPlayingMessage = null;
    };
  }
  

  scrollToBottom() {
    setTimeout(() => {
      this.chatBody.nativeElement.scrollTop = this.chatBody.nativeElement.scrollHeight;
    }, 100);
  }
}