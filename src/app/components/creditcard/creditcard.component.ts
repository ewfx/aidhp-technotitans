import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { NavbarComponent } from "../navbar/navbar.component";

@Component({
  selector: 'app-creditcard',
  imports: [CommonModule, ChatbotComponent, NavbarComponent],
  templateUrl: './creditcard.component.html',
  styleUrls: ['./creditcard.component.scss']
})
export class CreditCardComponent implements OnInit {
  creditCardRecommendation: any;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    const customerId = 'CUST001'; // Replace with actual ID
    this.http.get(`http://localhost:5000/recommend-credit-card/${customerId}`).subscribe(
      (response: any) => {
        if (response.status === 'success') {
          this.creditCardRecommendation = response;
        } else {
          console.error('Error fetching recommendations:', response.message);
        }
      },
      error => {
        console.error('API request failed:', error);
      }
    );
  }
}
