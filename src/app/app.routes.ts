import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { CreditCardComponent } from './components/creditcard/creditcard.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' }, 
  { path: 'login', component: LoginComponent }, 
  { path: 'home', component: HomeComponent }, 
  { path: 'credit', component: CreditCardComponent } // Add route for credit card page
]; 
