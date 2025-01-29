import { Routes } from '@angular/router';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { LibrarianDashboardComponent } from './components/librarian-dashboard/librarian-dashboard.component';
import { authGuard } from './auth.guard';
import { roleGuard } from './role.guard';
import { CheckinCheckoutComponent } from './components/librarian-dashboard/checkin-checkout/checkin-checkout.component';
import { ManageUsersComponent } from './components/librarian-dashboard/manage-users/manage-users.component';
import { ManageInventoryComponent } from './components/librarian-dashboard/manage-inventory/manage-inventory.component';
import { ManageReservationsComponent } from './components/librarian-dashboard/manage-reservations/manage-reservations.component';
import { ReportsComponent } from './components/librarian-dashboard/reports/reports.component';

export const routes: Routes = [
    {path: "", redirectTo: "login", pathMatch: "full"},
    {path: "sign-up", component: SignUpComponent},
    {path: "login", component: LoginComponent},
    {path: "home", component: HomeComponent, canActivate: [authGuard]},

    {
        path:"librarian-dashboard",
        component:LibrarianDashboardComponent,
        canActivate:[authGuard, roleGuard],
    children: [
        {path: "checkin-checkout", component: CheckinCheckoutComponent, canActivate: [authGuard, roleGuard]},
        {path: "manage-inventory", component: ManageInventoryComponent, canActivate: [authGuard, roleGuard]},
        {path: "manage-users", component: ManageUsersComponent, canActivate: [authGuard, roleGuard]},
        {path: "manage-reservations", component: ManageReservationsComponent, canActivate: [authGuard, roleGuard]},
        {path: "reports", component: ReportsComponent, canActivate: [authGuard, roleGuard]}
    ]}
];

export class AppComponent {}