import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';
import { ChatbotComponent } from '../chatbot/chatbot.component';
import { ChartDemoComponent } from '../../chart-demo/chart-demo.component';
import { Router } from '@angular/router';
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, NavbarComponent, ChatbotComponent, ChartDemoComponent],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent { 
  constructor(private router: Router) {}

  isLoginPage(): boolean {
    return this.router.url === '/login'; // ✅ Checks if login page is active
  }
}
