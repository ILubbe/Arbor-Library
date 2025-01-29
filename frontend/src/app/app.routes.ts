import { Routes } from '@angular/router';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { LibrarianDashboardComponent } from './components/librarian-dashboard/librarian-dashboard.component';
import { authGuard } from './auth.guard';
import { librarianGuard } from './librarian.guard';



export const routes: Routes = [
    {path:"", redirectTo:"login", pathMatch:"full"},
    {path:"sign-up", component:SignUpComponent},
    {path:"login", component:LoginComponent},
    {path:"home", component:HomeComponent, canActivate:[authGuard]},
    {path:"librarian-dashboard", component:LibrarianDashboardComponent, canActivate:[authGuard, librarianGuard]}
];
export class AppComponent {}