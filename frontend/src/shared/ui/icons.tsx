import * as React from "react"
import {
  FaFileAlt,
  FaFolder,
  FaPlus,
  FaPencilAlt,
  FaTrash,
  FaBolt,
  FaCrown,
  FaDesktop,
  FaMoon,
  FaUser,
  FaCreditCard,
  FaChartBar,
  FaSignOutAlt,
  FaShieldAlt,
  FaChalkboard,
  FaVideo,
  FaComment,
  FaBuilding,
  FaBox,
  FaHome,
  FaRocket,
  FaBook,
  FaPalette,
  FaHammer,
  FaSync,
  FaShoppingCart,
  FaCog,
  FaQuestionCircle,
  FaSave,
  FaQuoteRight,
  FaPaperclip,
  FaSun,
  FaFolderOpen
} from "react-icons/fa"

interface IconProps extends React.SVGProps<SVGSVGElement> {
  size?: number
}

// Posts and content icons
export function PostsIcon({ size = 16, ...props }: IconProps) {
  return <FaFileAlt size={size} {...props} />
}

export function CategoriesIcon({ size = 16, ...props }: IconProps) {
  return <FaFolder size={size} {...props} />
}

// Action icons
export function AddIcon({ size = 16, ...props }: IconProps) {
  return <FaPlus size={size} {...props} />
}

export function EditIcon({ size = 16, ...props }: IconProps) {
  return <FaPencilAlt size={size} {...props} />
}

export function DeleteIcon({ size = 16, ...props }: IconProps) {
  return <FaTrash size={size} {...props} />
}

export function SaveIcon({ size = 16, ...props }: IconProps) {
  return <FaSave size={size} {...props} />
}

export function RefreshIcon({ size = 16, ...props }: IconProps) {
  return <FaSync size={size} {...props} />
}

// Navigation icons
export function HomeIcon({ size = 16, ...props }: IconProps) {
  return <FaHome size={size} {...props} />
}

export function HubIcon({ size = 16, ...props }: IconProps) {
  return <FaQuoteRight size={size} {...props} />
}

export function SpaceIcon({ size = 16, ...props }: IconProps) {
  return <FaPaperclip size={size} {...props} />
}

export function CatalogIcon({ size = 16, ...props }: IconProps) {
  return <FaFolderOpen size={size} {...props} />
}

// User and account icons
export function UserIcon({ size = 16, ...props }: IconProps) {
  return <FaUser size={size} {...props} />
}

export function AdminIcon({ size = 16, ...props }: IconProps) {
  return <FaCrown size={size} {...props} />
}

export function LogoutIcon({ size = 16, ...props }: IconProps) {
  return <FaSignOutAlt size={size} {...props} />
}

// UI and system icons
export function SettingsIcon({ size = 16, ...props }: IconProps) {
  return <FaCog size={size} {...props} />
}

export function QuestionIcon({ size = 16, ...props }: IconProps) {
  return <FaQuestionCircle size={size} {...props} />
}

export function DemoIcon({ size = 16, ...props }: IconProps) {
  return <FaBolt size={size} {...props} />
}

// Theme icons
export function SunIcon({ size = 16, ...props }: IconProps) {
  return <FaSun size={size} {...props} />
}

export function MoonIcon({ size = 16, ...props }: IconProps) {
  return <FaMoon size={size} {...props} />
}

export function ComputerIcon({ size = 16, ...props }: IconProps) {
  return <FaDesktop size={size} {...props} />
}

// Business and commerce icons
export function CreditCardIcon({ size = 16, ...props }: IconProps) {
  return <FaCreditCard size={size} {...props} />
}

export function ShoppingIcon({ size = 16, ...props }: IconProps) {
  return <FaShoppingCart size={size} {...props} />
}

export function ChartIcon({ size = 16, ...props }: IconProps) {
  return <FaChartBar size={size} {...props} />
}

export function BuildingIcon({ size = 16, ...props }: IconProps) {
  return <FaBuilding size={size} {...props} />
}

// Content and media icons
export function BookIcon({ size = 16, ...props }: IconProps) {
  return <FaBook size={size} {...props} />
}

export function VideoIcon({ size = 16, ...props }: IconProps) {
  return <FaVideo size={size} {...props} />
}

export function MessageIcon({ size = 16, ...props }: IconProps) {
  return <FaComment size={size} {...props} />
}

export function WhiteboardIcon({ size = 16, ...props }: IconProps) {
  return <FaChalkboard size={size} {...props} />
}

// Tools and utilities icons
export function PaletteIcon({ size = 16, ...props }: IconProps) {
  return <FaPalette size={size} {...props} />
}

export function ConstructionIcon({ size = 16, ...props }: IconProps) {
  return <FaHammer size={size} {...props} />
}

export function BoxIcon({ size = 16, ...props }: IconProps) {
  return <FaBox size={size} {...props} />
}

export function ShieldIcon({ size = 16, ...props }: IconProps) {
  return <FaShieldAlt size={size} {...props} />
}

export function RocketIcon({ size = 16, ...props }: IconProps) {
  return <FaRocket size={size} {...props} />
}