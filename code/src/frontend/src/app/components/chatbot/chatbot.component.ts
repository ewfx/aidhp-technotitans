import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-chatbot',
  imports:[CommonModule,FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.scss']
})
export class ChatbotComponent {
  isOpen = false;
  userInput: string = '';
  messages: { text: string, sender: string }[] = [];

  constructor(private http: HttpClient) {}

  toggleChatbot() {
    this.isOpen = !this.isOpen;
   // Show the bot message only when opening the chatbot
   if (this.isOpen && this.messages.length === 0) {
    this.messages.push({ sender: 'bot', text: 'How may I help you today?' });
  }
}
  sendMessage() {
    if (!this.userInput.trim()) return;

    // Add user message
    this.messages.push({ text: this.userInput, sender: 'user' });

    // Send message to backend
    this.http.post<{ reply: string }>('http://localhost:5000/chat', { message: this.userInput }).subscribe(
      response => {
        this.messages.push({ text: response.reply, sender: 'bot' });
      },
      error => {
        console.error("Error fetching chatbot response:", error);
      }
    );

    this.userInput = ''; // Clear input field
  }
}
