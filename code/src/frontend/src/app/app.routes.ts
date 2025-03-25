import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { CreditCardComponent } from './components/creditcard/creditcard.component';
import { LoansComponent } from './components/loans/loans.component';
import { ProfileComponent } from './components/profile/profile.component';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' }, 
  { path: 'login', component: LoginComponent }, 
  { path: 'home', component: HomeComponent },
  { path: 'loans', component: LoansComponent}, 
  { path: 'credit', component: CreditCardComponent },
  { path: 'profile', component: ProfileComponent}
]; 
