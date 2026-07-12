/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class AssetFlowDashboard extends Component {
    setup() {
        this.notification = useService("notification");
        
        // Define reactive/stateful props with placeholder static data
        this.props = useState({
            menuItems: [
                { id: 'dashboard', name: 'Dashboard', icon: 'oi-view-list', isActive: true },
                { id: 'org_setup', name: 'Organization Setup', icon: 'oi-settings', isActive: false },
                { id: 'assets', name: 'Assets', icon: 'oi-tag', isActive: false },
                { id: 'allocation', name: 'Allocation & Transfer', icon: 'oi-shuffle', isActive: false },
                { id: 'booking', name: 'Resource Booking', icon: 'oi-calendar', isActive: false },
                { id: 'maintenance', name: 'Maintenance', icon: 'oi-wrench', isActive: false },
                { id: 'audit', name: 'Audit', icon: 'oi-check', isActive: false },
                { id: 'reports', name: 'Reports', icon: 'oi-graph', isActive: false },
                { id: 'notifications', name: 'Notifications', icon: 'oi-alert', isActive: false }
            ],
            kpiCards: [
                { id: 'avail', label: 'Assets Available', value: '27', icon: 'oi-check-circle', colorClass: 'blue' },
                { id: 'alloc', label: 'Assets Allocated', value: '56', icon: 'oi-arrow-right', colorClass: 'green' },
                { id: 'maint', label: 'Maintenance Today', value: '3', icon: 'oi-wrench', colorClass: 'yellow' },
                { id: 'booking', label: 'Active Bookings', value: '8', icon: 'oi-calendar', colorClass: 'cyan' },
                { id: 'transfer', label: 'Pending Transfers', value: '2', icon: 'oi-shuffle', colorClass: 'red' },
                { id: 'return', label: 'Upcoming Returns', value: '12', icon: 'oi-clock', colorClass: 'orange' }
            ],
            overdueAlert: {
                message: '1 Overdue returns active - flagged for follow-up'
            },
            activities: [
                { id: 1, desc: 'Laptop AF-0114 allocated to Priya from Engineering', time: '2 hours ago' },
                { id: 2, desc: 'Room B2 - booking confirmed - 2:00 to 3:00 PM', time: '4 hours ago' },
                { id: 3, desc: 'Projector AF-0056 - maintenance resolved', time: '1 day ago' }
            ]
        });
    }

    // Interactive event handler for sidebar nav navigation click (placeholder)
    onNavItemClick(itemId) {
        this.props.menuItems.forEach(item => {
            item.isActive = item.id === itemId;
        });
        this.notification.add(`Navigating to ${itemId} view (Placeholder)`, {
            type: "info",
            sticky: false,
        });
    }

    // Trigger helper on clicking quick action buttons
    onQuickAction(actionName) {
        let msg = "";
        if (actionName === 'register') {
            msg = "Opening Register Asset dialog (Developer 3 integration)...";
        } else if (actionName === 'book') {
            msg = "Redirecting to Resource Booking Scheduler...";
        } else if (actionName === 'maintenance') {
            msg = "Opening maintenance request ticket creation form...";
        }
        
        this.notification.add(msg, {
            title: "Quick Action Clicked",
            type: "success",
            sticky: false,
        });
    }
}

// Map the template string defined in XML
AssetFlowDashboard.template = "assetflow.DashboardTemplate";

// Register action inside Odoo client action list
registry.category("actions").add("assetflow_dashboard", AssetFlowDashboard);
