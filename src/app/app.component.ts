import { Component } from '@angular/core';

import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NavbarComponent } from './components/navbar/navbar.component';
import { ChatbotComponent } from './components/chatbot/chatbot.component';
import { ChartDemoComponent } from './chart-demo/chart-demo.component';

@Component({
  selector: 'app-root',
  imports: [CommonModule, RouterModule, NavbarComponent,ChatbotComponent,ChartDemoComponent], 
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {}
