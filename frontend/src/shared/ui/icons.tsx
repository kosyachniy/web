import * as React from "react"
import {
  FileText,
  FolderOpen,
  Plus,
  Pencil,
  Trash2,
  Zap,
  Crown,
  Monitor,
  Moon,
  User,
  CreditCard,
  BarChart3,
  LogOut,
  Shield,
  Presentation,
  Video,
  MessageSquare,
  Building2,
  Package,
  Home,
  Rocket,
  Book,
  Palette,
  Hammer,
  RotateCcw,
  ShoppingCart,
  Settings,
  HelpCircle,
  Save,
  Quote,
  Paperclip,
  Sun
} from "lucide-react"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

// Posts and content icons
export function PostsIcon({ size = 16, ...props }: IconProps) {
  return <FileText size={size} {...props} />
}

export function CategoriesIcon({ size = 16, ...props }: IconProps) {
  return <FolderOpen size={size} {...props} />
}

// Action icons
export function AddIcon({ size = 16, ...props }: IconProps) {
  return <Plus size={size} {...props} />
}

export function EditIcon({ size = 16, ...props }: IconProps) {
  return <Pencil size={size} {...props} />
}

export function DeleteIcon({ size = 16, ...props }: IconProps) {
  return <Trash2 size={size} {...props} />
}

export function SaveIcon({ size = 16, ...props }: IconProps) {
  return <Save size={size} {...props} />
}

export function RefreshIcon({ size = 16, ...props }: IconProps) {
  return <RotateCcw size={size} {...props} />
}

// Navigation icons
export function HomeIcon({ size = 16, ...props }: IconProps) {
  return <Home size={size} {...props} />
}

export function HubIcon({ size = 16, ...props }: IconProps) {
  return <Quote size={size} {...props} />
}

export function SpaceIcon({ size = 16, ...props }: IconProps) {
  return <Paperclip size={size} {...props} />
}

export function CatalogIcon({ size = 16, ...props }: IconProps) {
  return <FolderOpen size={size} {...props} />
}

// User and account icons
export function UserIcon({ size = 16, ...props }: IconProps) {
  return <User size={size} {...props} />
}

export function AdminIcon({ size = 16, ...props }: IconProps) {
  return <Crown size={size} {...props} />
}

export function LogoutIcon({ size = 16, ...props }: IconProps) {
  return <LogOut size={size} {...props} />
}

// UI and system icons
export function SettingsIcon({ size = 16, ...props }: IconProps) {
  return <Settings size={size} {...props} />
}

export function QuestionIcon({ size = 16, ...props }: IconProps) {
  return <HelpCircle size={size} {...props} />
}

export function DemoIcon({ size = 16, ...props }: IconProps) {
  return <Zap size={size} {...props} />
}

// Theme icons
export function SunIcon({ size = 16, ...props }: IconProps) {
  return <Sun size={size} {...props} />
}

export function MoonIcon({ size = 16, ...props }: IconProps) {
  return <Moon size={size} {...props} />
}

export function ComputerIcon({ size = 16, ...props }: IconProps) {
  return <Monitor size={size} {...props} />
}

// Business and commerce icons
export function CreditCardIcon({ size = 16, ...props }: IconProps) {
  return <CreditCard size={size} {...props} />
}

export function ShoppingIcon({ size = 16, ...props }: IconProps) {
  return <ShoppingCart size={size} {...props} />
}

export function ChartIcon({ size = 16, ...props }: IconProps) {
  return <BarChart3 size={size} {...props} />
}

export function BuildingIcon({ size = 16, ...props }: IconProps) {
  return <Building2 size={size} {...props} />
}

// Content and media icons
export function BookIcon({ size = 16, ...props }: IconProps) {
  return <Book size={size} {...props} />
}

export function VideoIcon({ size = 16, ...props }: IconProps) {
  return <Video size={size} {...props} />
}

export function MessageIcon({ size = 16, ...props }: IconProps) {
  return <MessageSquare size={size} {...props} />
}

export function WhiteboardIcon({ size = 16, ...props }: IconProps) {
  return <Presentation size={size} {...props} />
}

// Tools and utilities icons
export function PaletteIcon({ size = 16, ...props }: IconProps) {
  return <Palette size={size} {...props} />
}

export function ConstructionIcon({ size = 16, ...props }: IconProps) {
  return <Hammer size={size} {...props} />
}

export function BoxIcon({ size = 16, ...props }: IconProps) {
  return <Package size={size} {...props} />
}

export function ShieldIcon({ size = 16, ...props }: IconProps) {
  return <Shield size={size} {...props} />
}

export function RocketIcon({ size = 16, ...props }: IconProps) {
  return <Rocket size={size} {...props} />
}